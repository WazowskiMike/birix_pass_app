# web/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Главная и список категорий
    path('',                    views.category_list, name='category_list'),
    path('home/',                    views.index, name='index'),
    path('categories/',         views.category_list, name='category_list'),

    # Создать/редактировать/удалить категорию
    path('categories/add/',     views.category_form, name='category_add'),
    path('categories/<int:pk>/edit/',   views.category_form,   name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Список учёток и CRUD для них
    path('entries/',            views.entry_list, name='entry_list'),
    path('entries/add/',        views.entry_form, name='entry_add'),
    path('entries/<int:pk>/edit/',    views.entry_form,   name='entry_edit'),
    path('entries/<int:pk>/delete/',  views.entry_delete, name='entry_delete'),

    # Авторизация мастер-пароля
    path('login/',              views.login_view,   name='login'),
    path('logout/',             views.logout_view,  name='logout'),

    # Настройки — смена мастер-пароля
    path('settings/password/',  views.change_password, name='change_password'),
]
