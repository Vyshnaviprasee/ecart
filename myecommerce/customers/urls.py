from django.urls import path
from . import views

urlpatterns = [
    path ('show_accounts/', views.show_accounts, name='show_accounts'),
]