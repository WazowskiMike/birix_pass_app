from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('home/', views.index, name='index'),
    path('categories/', views.category_list, name='category_list'),

    path('categories/add/', views.category_form, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_form, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),

    path('entries/', views.entry_list, name='entry_list'),
    path('entries/add/', views.entry_form, name='entry_add'),
    path('entries/<int:pk>/edit/', views.entry_form, name='entry_edit'),
    path('entries/<int:pk>/delete/', views.entry_delete, name='entry_delete'),

    path('cards/', views.card_list, name='card_list'),
    path('cards/add/', views.card_form, name='card_add'),
    path('cards/<int:pk>/edit/', views.card_form, name='card_edit'),
    path('cards/<int:pk>/delete/', views.card_delete, name='card_delete'),

    # 🔥 Bank Accounts
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.account_form, name='account_add'),
    path('accounts/<int:pk>/edit/', views.account_form, name='account_edit'),
    path('accounts/<int:pk>/delete/', views.account_delete, name='account_delete'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('settings/password/', views.change_password, name='change_password'),
]
