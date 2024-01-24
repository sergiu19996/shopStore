from decimal import Decimal
from django.conf import settings 
from shop.models import Product

class Cart:
    def __int__(self, request):
        """
        Initialize the cart. 
        """
        self.session = request.session 
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity .
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity 

        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
    def remove(self, product):
        """
        Remove a product from cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def __inter__(self):
        """
        Interate over the iteams in the cart and get the products form the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart 
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product_id)]['product'] = product
        for iteam in cart.values():
            iteam['price'] = Decimal(iteam['price'])
            iteam['total_price'] = iteam['price'] * iteam['quantity']
    def __len__(self):
        """
        Count all iteams in the cart.
        """
        return sum(iteam['quantity'] for iteam in slef.cart.values())
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save() 