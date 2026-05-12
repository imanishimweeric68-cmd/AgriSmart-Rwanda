from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Order, OrderItem, Cart, CartItem
def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart
# HOME
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# PRODUCT DETAIL
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


# REGISTER
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")

    return render(request, "registration/register.html", {"form": form})


# ADD TO CART
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart = get_or_create_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        if item.quantity + 1 > product.stock:
            return render(request, 'cart.html', {
                'error': f"Only {product.stock} {product.name} available in stock"
            })
        item.quantity += 1
    else:
        if product.stock < 1:
            return render(request, 'cart.html', {
                'error': f"{product.name} is out of stock"
            })

    item.save()

    return redirect('cart_detail')


# CART PAGE
@login_required
def cart_detail(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()

    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# DECREASE CART
@login_required
def decrease_cart(request, id):
    cart = get_or_create_cart(request.user)

    item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=id
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_detail')


# REMOVE FROM CART
@login_required
def remove_from_cart(request, id):
    cart = get_or_create_cart(request.user)

    CartItem.objects.filter(
        cart=cart,
        product_id=id
    ).delete()

    return redirect('cart_detail')


# CHECKOUT
@login_required
def checkout(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()

    if not cart_items:
        return redirect('cart_detail')

    # Validate stock first
    for item in cart_items:
        if item.product.stock < item.quantity:
            return render(request, 'cart.html', {
                'error': f"Not enough stock for {item.product.name}"
            })

    # Create order
    order = Order.objects.create(user=request.user)

    # Create order items + reduce stock
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

        item.product.stock -= item.quantity
        item.product.save()

    # Clear cart
    cart_items.delete()

    return render(request, 'checkout_success.html', {
        'order': order
    })


# MY ORDERS
@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })
    
@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_detail')

    # 1. VALIDATE STOCK FIRST (IMPORTANT)
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)

        if product.stock < qty:
            return render(request, 'cart.html', {
                'error': f"Not enough stock for {product.name}"
            })

    # 2. CREATE ORDER
    order = Order.objects.create(user=request.user)

    # 3. CREATE ITEMS + REDUCE STOCK
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty
        )

        product.stock -= qty
        product.save()

    # 4. CLEAR CART
    request.session['cart'] = {}

    return render(request, 'checkout_success.html', {'order': order})