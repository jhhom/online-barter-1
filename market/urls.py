from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as  auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('market/', views.market, name='market'),
    path('add_item/', views.add_item, name='add_item'),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('traded_items/', views.traded_items, name='traded_items'),
    path('item/', views.item, name='item'),
    path('profile/', views.profile, name='profile')
]


