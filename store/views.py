from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

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


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'store/product_search_results.html', {'products': products, 'query': query})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:5]  # limit to 4

    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'store/product_detail.html', context)