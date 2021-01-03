from django.contrib import admin
from .models import Item, Profile, Barter

# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'condition', 'description', 'image')
    list_filter = ('title', 'condition')
    search_fields = ('title', 'condition')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo')
    search_fields = ('user',)

@admin.register(Barter)
class BarterAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'offer', 'requested_by', 'requested_date', 'status')