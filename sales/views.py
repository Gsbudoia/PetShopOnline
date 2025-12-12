from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Sale, SaleItem
from .cart import Cart # Importa a classe que acabamos de 
from django.views.decorators.http import require_POST

# --- LISTA DE PRODUTOS (VITRINE) ---
def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'sales/product_list.html', {'products': products})

# --- ADICIONAR AO CARRINHO ---
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1        
    # Adiciona ao carrinho com a quantidade escolhida
    cart.add(product=product, quantity=quantity)
    
    return redirect('cart_detail')

# --- REMOVER DO CARRINHO ---
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

# --- VER CARRINHO ---
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'sales/cart_detail.html', {'cart': cart})

# --- FINALIZAR PEDIDO (FECHAR A VENDA) ---
@login_required(login_url='/accounts/login/')
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        # 1. Cria a Venda no Banco
        order = Sale.objects.create(
            customer=request.user.customer,
            seller=request.user, # Num e-commerce puro, o seller seria o Admin ou null
            is_closed=True
        )
        
        # 2. Transfere itens do Carrinho (Sessão) para o Banco (SaleItem)
        for item in cart:
            SaleItem.objects.create(
                sale=order,
                product=item['product'],
                unit_price=item['price'],
                quantity=item['quantity']
            )
            
        # 3. Limpa o carrinho e avisa
        cart.clear()
        return render(request, 'sales/order_created.html', {'order': order})
    
    return redirect('cart_detail')

def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Pega o número que veio do formulário
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
    
    # Se o cliente colocou 0, removemos o produto. Se for > 0, atualizamos.
    if quantity > 0:
        # update_quantity=True força o carrinho a substituir o valor (ex: de 5 vira 3)
        cart.add(product=product, quantity=quantity, update_quantity=True)
    else:
        cart.remove(product)
        
    return redirect('cart_detail')