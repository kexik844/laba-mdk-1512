class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def set_qty(self, product_id, qty):
        product_id = str(product_id)
        if qty <= 0:
            self.remove(product_id)
        else:
            self.cart[product_id] = qty
            self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())

    def get_total_price(self):
        from .models import Product
        total = 0
        for product_id, qty in self.cart.items():
            product = Product.objects.get(id=int(product_id))
            total += product.price * qty
        return total

    def get_items(self):
        from .models import Product
        items = []
        for product_id, qty in self.cart.items():
            product = Product.objects.get(id=int(product_id))
            items.append({
                'product': product,
                'quantity': qty,
                'total': product.price * qty
            })
        return items