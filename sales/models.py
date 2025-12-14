from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import Customer
from django.conf import settings # Para pegar o usuário logado

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagem")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    stock_quantity = models.IntegerField(verbose_name="Quantidade em Estoque")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Vendedor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Venda")
    is_closed = models.BooleanField(default=False, verbose_name="Venda Fechada?")

    def get_total(self):
        # Lógica para calcular o total somando os itens
        return sum(item.get_subtotal() for item in self.items.all())

    def __str__(self):
        return f"Venda #{self.id} - {self.created_at.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produto")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")
    # O preço unitário é salvo aqui para histórico. Se o produto aumentar de preço amanhã, 
    # a venda antiga não pode mudar de valor.

    def get_subtotal(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        # Requisito: Validação de Dados
        if not self.pk: # Apenas na criação
            if self.product.stock_quantity < self.quantity:
                raise ValidationError(f"Estoque insuficiente para {self.product.name}. Disponível: {self.product.stock_quantity}")
            
            # Preenche o preço automaticamente baseado no cadastro do produto
            self.unit_price = self.product.price
            
            # Abate do estoque (Simples)
            self.product.stock_quantity -= self.quantity
            self.product.save()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"