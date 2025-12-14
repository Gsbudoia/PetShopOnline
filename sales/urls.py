from django.urls import path
from . import views

urlpatterns = [
    path('loja/', views.product_list, name='product_list'),
    path('carrinho/', views.cart_detail, name='cart_detail'),
    path('adicionar/<int:product_id>/', views.cart_add, name='cart_add'),
    path('atualizar/<int:product_id>/', views.cart_update, name='cart_update'),
    path('remover/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('finalizar/', views.order_create, name='order_create'),
    path('gestao/estoque/', views.admin_stock_list, name='admin_stock_list'),
    path('gestao/produto/novo/', views.admin_product_add, name='admin_product_add'),
    path('gestao/produto/remover/<int:pk>/', views.admin_product_delete, name='admin_product_delete'),
]