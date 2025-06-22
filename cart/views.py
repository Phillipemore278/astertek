from django.shortcuts import get_object_or_404,render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from .models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    cart_items = list(cart)  # __iter__ gives you all cart items
    cart_total = cart.get_total_price()
    
    return render(request, 'cart/cart_summary.html', {
        'cart_items': cart_items,
        'cart_total': f"{cart_total:.2f}",
        'shipping': cart.get_shipping_cost(),
        'final_total': cart.get_final_total(),
    })


@require_POST
def cart_add_ajax(request):
    slug = request.POST.get('slug')
    quantity = request.POST.get('quantity', 1)

    if not slug:
        return JsonResponse({'success': False, 'error': 'No product slug provided'})
    
    try:
        product = Product.objects.get(slug=slug)
        quantity = int(quantity)
        cart = Cart(request)
        cart.add(product=product, quantity=quantity)
        return JsonResponse({
            'success': True,
            'cartCount': len(cart),
            'message': f'Added {product.name} (x{quantity}) to cart.'
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    

@require_POST
def cart_update_ajax(request):
    slug = request.POST.get('slug')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, slug=slug)

    cart = Cart(request)
    cart.add(product, quantity=quantity, override_quantity=True)

    item_total = 0
    for item in cart:
        if product.id == item['product_obj'].id:
            item_total = item['total_price']
            break

    return JsonResponse({
        'success': True,
        'itemTotal': f'{item_total:.2f}',
        'cartTotal': f'{cart.get_total_price():.2f}',
        'finalTotal': f'{cart.get_final_total():.2f}',
        'cartCount': len(cart),
    })


@require_POST
def cart_remove_ajax(request):
    slug = request.POST.get('slug')
    product = get_object_or_404(Product, slug=slug)

    cart = Cart(request)
    cart.remove(product)

    return JsonResponse({
        'success': True,
        'cartTotal': f'{cart.get_total_price():.2f}',
        'finalTotal': f'{cart.get_final_total():.2f}',
        'cartCount': len(cart),
        
    })


# @login_required
def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect(f"{reverse('account:auth_choice')}?next={request.path}")
    
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('cart:cart_detail')  # Prevent checkout with empty cart

    cart_items = list(cart)
    cart_total = cart.get_total_price()
    shipping = 2500  # flat rate for now
    final_total = cart_total + shipping

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping': shipping,
        'final_total': final_total,
    })


@login_required
def process_checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        email = request.POST.get('email')

        # TODO: Save order to DB (you can build an Order model later)

        # Clear cart
        cart = Cart(request)
        cart.clear()

        messages.success(request, "Order placed successfully!")
        return redirect('frontend:home')

    return redirect('cart:checkout')
