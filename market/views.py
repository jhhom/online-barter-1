from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .forms import AddItemForm, UserRegistrationForm, UserUpdateForm, \
    ProfileUpdateForm, ItemSearchForm, ItemSortForm, ItemFilterForm
from .models import Item, Barter
from django.core.paginator import Paginator
from django.contrib import messages

import statistics

def index(request):
    return render(request, 'index.html')

# Create your views here.
@login_required
def profile(request):
    ready_items = Item.objects.filter(owner=request.user)
    exchanged_items = [barter.item for barter in Barter.objects.filter(status='SC', item__owner=request.user)]
    if len(ready_items) > 4:
        ready_items = ready_items[:4]
    if len(exchanged_items) > 4:
        exchanged_items = exchanged_items[:4]

    print(exchanged_items)
    context = {
        'user': request.user,
        'ready_items': ready_items,
        'exchanged_items': exchanged_items
    }
    return render(request, 'profile.html', context)

@login_required
def traded_items(request):
    traded_items = Item.objects.filter(owner=request.user)
    barter_requests = Barter.objects.filter(item__owner=request.user, status='PN')
    sent_requests = Barter.objects.filter(offer__owner=request.user, status='PN')
    completed_trades = Barter.objects.filter(
        Q(item__owner=request.user) | Q(offer__owner=request.user),
        status='SC'
    )
    favourites = Item.objects.filter(favourited_by=request.user)
    categories = Item.ITEM_CATEGORIES
    delete_status = False

    if request.method == 'POST':
        action_code = request.POST['id'][0]
        object_id = request.POST['id'][1:]

        if action_code == 'D':
            item = Item.objects.filter(id=object_id).delete()
            messages.success(request, 'Sucessfully deleted item.')
            delete_status = True
        # accept barter request
        elif action_code == 'A':
            Barter.objects.filter(id=object_id).update(status='SC')
        elif action_code == 'R':
            Barter.objects.filter(id=object_id).update(status='RJ')
        elif action_code == 'C':
            Barter.objects.filter(id=object_id).delete()

    context = {
        'items': traded_items,
        'barter_requests': barter_requests,
        #'delete_status': delete_status,
        'sent_requests': sent_requests,
        'completed_trades': completed_trades,
        'favourites': favourites,
        'categories': categories
    }
    return render(request, 'traded_items.html', context)

@login_required
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.owner = request.user
            new_item.save()
            messages.success(request, 'Sucessfully added item.')
            return redirect('traded_items')
    else:
        form = AddItemForm()
    return render(request, 'add_item.html', {'form': form})

@login_required
def update_item(request, item_id):
    try:
        item_sel = Item.objects.get(id = item_id)
    except Item.DoesNotExist:
        return redirect('traded_items')
    form = AddItemForm(request.POST or None, instance = item_sel)
    if form.is_valid():
       form.save()
       messages.success(request, 'Sucessfully updated item.')
       return redirect('traded_items')
    return render(request, 'add_item.html', {'form':form,'item':item_sel})

@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                        instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile) 

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
        
    return render(request, 'settings.html', context)
        

def market(request):
    search_form = ItemSearchForm()
    sort_form = ItemSortForm()
    filter_form = ItemFilterForm()
    term = None
    sort_by = None
    filter = None
    results = Item.objects.all()

    if 'term' in request.GET:
        search_form = ItemSearchForm(request.GET)
        if search_form.is_valid():
            term = search_form.cleaned_data['term']
            results = Item.objects.filter(title__contains=term)
            if request.user.is_authenticated:
                try:
                    most_favourited = statistics.mode(
                        [item.category for item in Item.objects.filter(favourited_by=request.user)]
                    )
                    results \
                        .extra(select={'match': f'category="{most_favourited}"'}) \
                        .order_by('-match')
                except:
                    pass
    
    if 'sort_by' in request.GET:
        sort_form = ItemSortForm(request.GET)
        if sort_form.is_valid():
            sort_by = sort_form.cleaned_data['sort_by']
            if sort_by == 'TL':
                results = results.order_by('title')
            elif sort_by == 'DT':
                results = results.order_by('listed_date')
            elif sort_by == 'PL':
                results = results \
                    .annotate(favourite_count=Count('favourited_by')) \
                    .order_by('favourite_count')
    
    if ('condition_filter' in request.GET) or ('category_filter' in request.GET):
        filter_form = ItemFilterForm(request.GET)
        condition_filter = filter_form['condition_filter'].value()
        category_filter = filter_form['category_filter'].value()
        print(condition_filter)
        print(category_filter)
        if condition_filter != None:
            results = results.filter(condition=condition_filter)
        if category_filter != None:
            results = results.filter(category=category_filter)
   
    paginator = Paginator(results, 6) # Show 6 items per page.
    page_number = request.GET.get('page',1)
    page_obj = paginator.page(page_number)

    context = {
        'search_form': search_form,
        'sort_form': sort_form,
        'filter_form': filter_form,
        'term': term,
        'sort_by': sort_by,
        'filter': filter,
        'categories': Item.ITEM_CATEGORIES,
        'items': page_obj,
    }
    return render(request, 'market.html', context)

def success(request):
    return HttpResponse('Successfully uploaded')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('profile', permanent=True)
    else:
        user_form = UserRegistrationForm()
    return render(request,
                'register.html',
                {'user_form': user_form})

def item(request):
    id = request.GET['id']
    item = get_object_or_404(Item, id=id)
    listed_items = Item.objects.filter(owner=request.user)
    is_favourite = None
    barter_request_sent = False
    try:
        is_favourite = item.favourited_by \
            .get(id=request.user.id)
    except:
        pass

    if is_favourite == None:
        is_favourite = False
    else:
        is_favourite = True
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        listed_items = Item.objects.filter(owner=request.user)
        try:
            _ = request.POST['favourite']
        except:
            bartered_item_id = request.POST['exchanged-item']
            # b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
            bartered_item = Item.objects.get(id=bartered_item_id)
            barter = Barter(item=item ,offer=bartered_item, requested_by=request.user)
            barter.save()
            barter_request_sent = True

        if is_favourite:
            item.favourited_by.remove(request.user)
        else:
            item.favourited_by.add(request.user)
        is_favourite = not is_favourite


    context = {
        'item': item,
        'is_favourite': is_favourite,
        'categories': Item.ITEM_CATEGORIES,
        'listed_items': listed_items,
        'barter_request_sent': barter_request_sent,
    }
    return render(request, 'item.html', context)
