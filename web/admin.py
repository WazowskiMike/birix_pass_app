from django.contrib import admin
from .models import MasterConfig, Category, Entry

@admin.register(MasterConfig)
class MasterConfigAdmin(admin.ModelAdmin):
    # Показываем в списке ид и хэш текущего мастер-пароля
    list_display = ('id', 'password_hash',)
    # Делаем поле password_hash только для чтения
    readonly_fields = ('password_hash',)

    # Именованная секция, чтобы не падало, если у вас нет дат
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