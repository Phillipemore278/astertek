from django.urls import path

from . import views
app_name = 'store'
urlpatterns = [
    path('', views.store, name='store'),
    path('search/', views.product_search, name='product_search'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]