from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('edit/', views.edit_profile, name='edit_profile'),
]
