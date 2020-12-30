from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import AddItemForm, LoginForm, UserRegistrationForm
from .models import Item

# Create your views here.
@login_required
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse('Successfully uploaded')
    else:
        form = AddItemForm()
    return render(request, 'add_item.html', {'form': form})

def market(request):
    items = Item.objects.all()
    return render(request, 'market.html', {'items': items})

def success(request):
    return HttpResponse('Successfully uploaded')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                        'register_done.html',
                        {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                'register.html',
                {'user_form': user_form})