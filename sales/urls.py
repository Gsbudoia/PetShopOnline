from django.urls import path
from . import views

urlpatterns = [
    path('loja/', views.product_list, name='product_list'),
    path('carrinho/', views.cart_detail, name='cart_detail'),
    path('adicionar/<int:product_id>/', views.cart_add, name='cart_add'),
    path('atualizar/<int:product_id>/', views.cart_update, name='cart_update'),
    path('remover/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('finalizar/', views.order_create, name='order_create'),
]