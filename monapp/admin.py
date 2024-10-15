from django.contrib import admin
from .models import Product, ProductItem, ProductAttribute, ProductAttributeValue, Fournisseur, PrixProduct, Order

def set_product_online(modeladmin, request, queryset):
    queryset.update(status=1)
set_product_online.short_description = "Mettre en ligne"
def set_product_offline(modeladmin, request, queryset):
    queryset.update(status=0)
set_product_offline.short_description = "Mettre hors ligne"

class ProductItemAdmin(admin.TabularInline):
    model = ProductItem
    filter_vertical = ("attributes",)
    raw_id_fields = ["attributes"]

class ProductAdmin(admin.ModelAdmin):
    model =  Product
    inlines = [ProductItemAdmin,]
    list_display = ("id", "name", "price_ht", "price_ttc", "code")
    list_editable = ["name", "price_ht", "price_ttc"]
    radio_fields = {"status":admin.VERTICAL}
    search_fields = ('name', 'status')
    list_filter = ("status", "date_creation")
    date_hierarchy = 'date_creation'
    ordering = ('-date_creation',)
    actions = [set_product_online, set_product_offline]
 

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(PrixProduct)
admin.site.register(Fournisseur)
admin.site.register(Order)
