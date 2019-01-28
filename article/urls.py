from django.urls import path, include
from django.shortcuts import render
from .views import (
    IndexView, DetailView, OutUser,
    ContactView, PasswordReset, thanks,
    add_article, add_comment, activate,
    signup, account_activation_sent
)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', DetailView.as_view(), name='detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/thanks', thanks, name='thanks'),
    path('accounts/logout/', OutUser.as_view(), name='log'),
    path('accounts/password_reset/', PasswordReset.as_view(), name='reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('article/create/', add_article, name='create_art'),
    path('article/<int:pk>/comment/create/', add_comment, name='create_com'),
    path('signup/', signup, name='signup'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<token>/<uidb64>/', activate, name='activate'),
]
