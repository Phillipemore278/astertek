from decimal import Decimal
from django.conf import settings
from .models import Product, CartItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        # Session cart update
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'name': product.name,
                'slug': product.slug,
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

        # DB cart update for logged-in users
        if self.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(user=self.user, product=product)
            if override_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user, product=product).delete()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user).delete()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item['product_obj'] = product
            cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
            yield cart_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def sync_to_session(self):
        # Sync DB cart items to session cart on login
        if self.user.is_authenticated:
            self.cart = {}
            for item in CartItem.objects.filter(user=self.user):
                self.cart[str(item.product.id)] = {
                    'quantity': item.quantity,
                    'price': str(item.product.price),
                    'name': item.product.name,
                    'slug': item.product.slug,
                }
            self.save()
