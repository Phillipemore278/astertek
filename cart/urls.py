from django.urls import path

from . import views
app_name = 'cart'
urlpatterns = [
    path('add-ajax/', views.cart_add_ajax, name='cart_add_ajax'),
]