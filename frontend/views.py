from django.shortcuts import render

# my imports
from store.models import Product

def home(request):
    deals_products = Product.objects.filter(tags__name__iexact='Deals of the week', is_available=True)
    new_products = Product.objects.filter(tags__name__iexact='Recent Products', is_available=True)
    onsale_products = Product.objects.filter(tags__name__iexact='On Sale', is_available=True)
    featured_products = Product.objects.filter(tags__name__iexact='Featured Products', is_available=True)

    earphone_products = Product.objects.filter(tags__name__iexact='Ear Phones', is_available=True)
    mouse_products = Product.objects.filter(tags__name__iexact='Mouse', is_available=True)

    context = {
        'deals_products': deals_products,
        'new_products': new_products,
        'onsale_products': onsale_products,
        'featured_products': featured_products,
        'earphone_products': earphone_products,
        'mouse_products': mouse_products,
    }
    return render(request, 'frontend/index.html', context)
