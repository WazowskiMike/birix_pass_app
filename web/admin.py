from django.contrib import admin
from .models import MasterConfig, Category, Entry

@admin.register(MasterConfig)
class MasterConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'password_hash',)
    readonly_fields = ('password_hash',)

    fieldsets = (
        (None, {
            'fields': ('password_hash',),
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'username', 'category']