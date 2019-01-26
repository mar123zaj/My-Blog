from django.urls import path
from .views import IndexView, DetailView, OutUser, ContactView, PasswordReset

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', DetailView.as_view(), name='detail'),
    path('accounts/logout/', OutUser.as_view(), name='log'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('accounts/password_reset/', PasswordReset.as_view(), name='reset'),

]
