from django.contrib.auth.models import User
from django import forms
from .models import Item, Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone', 'photo']


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'condition', 'description', 'image','category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-input'}),
            'condition': forms.Select(attrs={'class': 'condition-input'}),
            'description': forms.Textarea(attrs={'class': 'description-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'image-input'}),
            'category':forms.Select(attrs={'class':'category-input'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ItemSearchForm(forms.Form):
    term = forms.CharField(label='Search',
                        required=False,
                        widget=forms.TextInput(attrs={'placeholder': 'Search for items'}))

class ItemSortForm(forms.Form):
    SORT_MODES = (
        ('TL', 'Title'),
        ('DT', 'Listed Date'),
        ('PL', 'Popularity')
    )
    sort_by = forms.ChoiceField(choices=SORT_MODES,
                            widget=forms.Select(attrs={'onchange': 'this.form.submit()'}))


class ItemFilterForm(forms.Form):
    condition_filter = forms.ChoiceField(
        choices=Item.ITEM_CONDITION_CHOICES,
        widget=forms.RadioSelect(attrs={'onchange': 'this.form.submit()'})
    )
    category_filter = forms.ChoiceField(
        choices=Item.ITEM_CATEGORIES,
        widget=forms.RadioSelect(attrs={'onchange': 'this.form.submit()'})
    )