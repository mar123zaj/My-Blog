from django.urls import path
from .views import IndexView, DetailView, OutUser

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', DetailView.as_view(), name='detail'),
    path('accounts/logout/', OutUser.as_view(), name='log'),\
]
