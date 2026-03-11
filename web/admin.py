from django.contrib import admin

from .models import Category, Products, Cart, Profile, WishList, Checkout, DefaultImages, Order

class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('product',)  # or use filter_vertical
    list_display = ('name', 'quantity')


class ProductsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code',]  # Add any fields you want searchable
    list_display = ['name', 'code', 'sellp', 'quantity_in_stock']  # Optional: show these columns
    list_filter = ['active']  # Optional: add filters on the sidebar


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Cart)
admin.site.register(Profile)
admin.site.register(WishList)
admin.site.register(Checkout)
admin.site.register(DefaultImages)
admin.site.register(Order)