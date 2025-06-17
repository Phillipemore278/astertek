from django.shortcuts import render

# my imports
from store.models import Product

def home(request):
    deals_products = Product.objects.filter(tags__name__iexact='Deals of the week', is_available=True)

    context = {
        'deals_products': deals_products,
    }
    return render(request, 'frontend/index.html', context)
