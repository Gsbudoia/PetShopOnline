from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        """
        Inicializa o carrinho.
        """
        self.session = request.session
        cart = self.session.get('carrinho_sessao')
        
        if not cart:
            # Salva um carrinho vazio na sessão se não existir
            cart = self.session['carrinho_sessao'] = {}
        
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Adiciona um produto ao carrinho ou atualiza a quantidade.
        """
        product_id = str(product.id) # JSON só aceita chaves string
        
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        self.save()

    def remove(self, product):
        """
        Remove um produto do carrinho.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Percorre os itens do carrinho e pega os produtos do banco de dados.
        """
        product_ids = self.cart.keys()
        # Pega os produtos reais do banco de uma vez só
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        """
        Calcula o valor total da compra.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Remove o carrinho da sessão
        del self.session['carrinho_sessao']
        self.save()

    def save(self):
        # Marca a sessão como modificada para garantir que o Django salve
        self.session.modified = True