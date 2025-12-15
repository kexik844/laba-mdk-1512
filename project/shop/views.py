from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Category, Product, Order, OrderItem
from .forms import CheckoutForm
from .cart import Cart

def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)[:6]
    context = {
        'categories': categories,
        'products': products,
        'title': 'Главная'
    }
    return render(request, 'shop/index.html', context)

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    search = request.GET.get('search', '')
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
    
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)
    
    context = {
        'category': category,
        'products': products,
        'search': search,
        'sort': sort,
    }
    return render(request, 'shop/category.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related': related
    }
    return render(request, 'shop/product_detail.html', context)

def cart_view(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'items': cart.get_items(),
        'total': cart.get_total_price(),
        'count': len(cart)
    }
    return render(request, 'shop/cart.html', context)

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    qty = int(request.POST.get('quantity', 1))
    cart.add(product_id, qty)
    messages.success(request, f'{product.name} добавлен в корзину!')
    return redirect('shop:cart')

@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('shop:cart')

@require_POST
def update_cart(request, product_id):
    qty = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.set_qty(product_id, qty)
    return redirect('shop:cart')

def checkout(request):
    cart = Cart(request)
    if len(cart.cart) == 0:
        return redirect('shop:cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            
            for product_id, qty in cart.cart.items():
                product = Product.objects.get(id=int(product_id))
                if product.stock < qty:
                    messages.error(request, f'Недостаточно товара: {product.name}')
                    order.delete()
                    return redirect('shop:checkout')
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price_at_purchase=product.price
                )
                product.stock -= qty
                product.save()
            
            cart.clear()
            messages.success(request, f'Заказ #{order.id} успешно создан!')
            return redirect('shop:order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'items': cart.get_items(),
        'total': cart.get_total_price()
    }
    return render(request, 'shop/checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'shop/order_confirmation.html', context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'shop/my_orders.html', context)