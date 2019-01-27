from django.urls import path, include
from django.shortcuts import render
from .views import (
    IndexView, DetailView, OutUser,
    ContactView, PasswordReset, thanks,
    CreateArticle, add_comment
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', DetailView.as_view(), name='detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/thanks', thanks, name='thanks'),
    path('accounts/logout/', OutUser.as_view(), name='log'),
    path('accounts/password_reset/', PasswordReset.as_view(), name='reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('article/create/', CreateArticle.as_view(), name='create_art'),
    path('article/<int:pk>/comment/create/', add_comment, name='create_com'),
    path('/activate/<slug:uidb64>/<slug:token>/', add_comment, name='create_com'),
]
