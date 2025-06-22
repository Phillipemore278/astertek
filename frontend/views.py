from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

# my imports
from store.models import Category, Product, Brand, Tag

def home(request):
    all_products = Product.objects.all()
    deals_products = Product.objects.filter(tags__name__iexact='Deals of the week', is_available=True)
    new_products = Product.objects.filter(tags__name__iexact='Recent Products', is_available=True)
    onsale_products = Product.objects.filter(tags__name__iexact='On Sale', is_available=True)
    featured_products = Product.objects.filter(tags__name__iexact='Featured Products', is_available=True)

    earphone_products = Product.objects.filter(tags__name__iexact='Ear Phones', is_available=True)
    mouse_products = Product.objects.filter(tags__name__iexact='Mouse', is_available=True)

    context = {
        'all_products': all_products,
        'deals_products': deals_products,
        'new_products': new_products,
        'onsale_products': onsale_products,
        'featured_products': featured_products,
        'earphone_products': earphone_products,
        'mouse_products': mouse_products,
    }
    return render(request, 'frontend/index.html', context)


# def category_list(request):
#     categories = Category.objects.all()
#     return render(request, "frontend/category_list.html", {"categories": categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product_list = Product.objects.filter(category=category)

    # Pagination: 9 products per page (you can change this)
    paginator = Paginator(product_list, 15)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    brands = Brand.objects.all()
    tags = Tag.objects.all()

    context = {
        "category": category,
        'products': products,  # This is now a Page object
        'brands': brands,
        'tags': tags,
    }
    return render(request, "frontend/category_detail.html", context)


def about(request):
    return render(request, 'frontend/about.html' )


def contact(request):
    return render(request, 'frontend/contact.html' )

