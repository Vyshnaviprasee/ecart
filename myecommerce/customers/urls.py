from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path ('show_accounts/', views.show_accounts, name='show_accounts'),
    path ('logout/', views.logout, name='logout'),
    
]