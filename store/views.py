from django.core.paginator import Paginator
from django.shortcuts import render

from store.models import Product

def store(request):
    product_list = Product.objects.all()

    # Pagination: 9 products per page (you can change this)
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products':products
    }
    return render(request, 'store/store.html', context)
