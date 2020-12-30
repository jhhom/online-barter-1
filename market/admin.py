from django.contrib import admin
from .models import Item, Profile

# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'condition', 'description', 'image')
    list_filter = ('title', 'condition')
    search_fields = ('title', 'condition')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo')
    search_fields = ('user',)