from django.urls import path
from .api_views import *
urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('cart/', CartAPIView.as_view(), name='cart-list'),
    path('addtocart/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('product/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('category/<str:name>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('search/', SearchProductsAPIView.as_view(), name='search-products'),
    path('remove/fromcart/', RemoveFromCartAPIView.as_view(), name='delete-from-cart'),
    #path('update/cartitem/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
    #path('clear/cart/', ClearCartAPIView.as_view(), name='clear-cart'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('addtocheckout/', AddToCheckoutAPIView.as_view(), name='add-to-checkout'),
    #path('wishlist/', WishListAPIView.as_view(), name='wishlist'),
    #path('addtowishlist/', AddToWishListAPIView.as_view(), name='add-to-wishlist'),
    path('remove/fromwishlist/', RemoveFromWishListAPIView.as_view(), name='remove-from-wishlist'),
]