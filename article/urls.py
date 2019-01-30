from django.urls import path, include
from .views import (
    IndexView, DetailView, OutUser,
    ContactView, PasswordReset, thanks,
    add_article, add_comment, activate,
    signup, account_activation_sent, EditProfile,
    view_profile, edit_comment,
    about, delete_comment
)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', DetailView.as_view(), name='detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/thanks/', thanks, name='thanks'),
    path('accounts/logout/', OutUser.as_view(), name='log'),
    path('accounts/password_reset/', PasswordReset.as_view(), name='reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('article/create/', add_article, name='create_art'),
    path('article/<int:pk>/comment/create/', add_comment, name='create_com'),
    path('signup/', signup, name='signup'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<token>/<uidb64>/', activate, name='activate'),
    path('profile/<int:pk>/', view_profile, name='profile'),
    path('profile/edit/<int:pk>/', EditProfile.as_view(), name='edit_profile'),
    path('article/comment/edit/<int:pk>/', edit_comment, name='edit_comment'),
    path('article/comment/delete/<int:pk>/', delete_comment, name='delete_comment'),
    path('about/', about, name='about'),

]
