from django.contrib import admin

from .models import Asset, Task


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'location', 'last_updated')
    list_filter = ('status',)
    search_fields = ('name', 'location')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
