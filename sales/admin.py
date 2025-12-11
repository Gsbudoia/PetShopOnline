from django.contrib import admin
from .models import Product, Sale, SaleItem

# Isso permite adicionar itens na venda DENTRO da tela da venda
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1 # Quantas linhas vazias aparecem
    readonly_fields = ('unit_price',) # Preço unitário não deve ser editado manualmente aqui

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    # Fieldsets organizam os campos em seções azuis
    fieldsets = (
        ('Dados da Venda', {
            'fields': ('customer', 'seller', 'is_closed')
        }),
        ('Datas', {
            'fields': ('created_at',),
            'classes': ('collapse',) # Esconde essa seção para economizar espaço
        }),
    )
    
    # Coloca a tabela de itens dentro da venda
    inlines = [SaleItemInline]
    
    # Filtros laterais e pesquisa
    list_display = ('id', 'customer', 'created_at', 'get_total_display', 'is_closed')
    list_filter = ('is_closed', 'created_at')
    search_fields = ('customer__name',)
    readonly_fields = ('created_at',)

    # Método para mostrar o total na lista do admin
    def get_total_display(self, obj):
        return f"R$ {obj.get_total()}"
    get_total_display.short_description = "Total"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'is_active')
    list_editable = ('price', 'stock_quantity') # Permite editar preço direto na lista!
    search_fields = ('name',)