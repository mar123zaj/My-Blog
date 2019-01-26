from django.urls import path, include
from django.shortcuts import render
from .views import IndexView, DetailView, OutUser, ContactView, PasswordReset, thanks

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', DetailView.as_view(), name='detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/thanks', thanks, name='thanks'),
    path('accounts/logout/', OutUser.as_view(), name='log'),
    path('accounts/password_reset/', PasswordReset.as_view(), name='reset'),
    path('accounts/', include('django.contrib.auth.urls')),
]
