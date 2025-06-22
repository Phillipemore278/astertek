from django.urls import path

from . import views
app_name = 'account'
urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('auth-choice/', views.auth_choice_view, name='auth_choice'),
]