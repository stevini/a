from django.urls import path
from . import views
from .api_views import *
from django_daraja.views import stk_push_success


urlpatterns = [
    #BINGO
    path('404/', views.view404, name='notfound'),
    path('about/', views.about),
    path('cart/', views.cart),
    path('category/', views.category_view),
    path('category/<str:name>/', views.category),
    path('checkout/', views.checkout),
    path('comingsoon/', views.comingSoon),
    path('contact/', views.contact),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index),
    path('home/', views.index13),
    path('login/', views.login_view, name='login'),
    #path('register/', views.register, name='register'),
    path('productfullwidth/', views.productCategoryFullwidth),
    path('product/<str:name>/', views.product),
    path('wishlist/', views.wishlist),
    path('logout/', views.user_logout, name='logout'),
    path('add/<str:name>/', views.add_to_cart, name='add'),
    path('remove/<str:name>/', views.remove_from_cart, name='remove'),
    path('addwishlist/<str:name>/', views.add_to_wishlist, name='addwishlist'),
    path('removewishlist/<str:name>/', views.remove_from_wishlist, name='removewishlist'),
    path('cartfromwishlist/<str:name>/', views.cart_from_wishlist, name='cartfromwishlist'),
    path('addtocheckout/', views.add_to_checkout, name='addtocheckout'),
    path('placeorder/', views.place_order, name='place_order'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('removefrmcheckout/<str:name>/', views.remove_from_checkout, name='removefrmcheckout'),
    path('clearcheckout/', views.delete_checkout, name='clearcheckout'),
    path('search/', views.search_product, name='search'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('checkouttest/', views.checkout_test, name='checkouttest'),
    path('listproducts/', views.listProducts, name='listproducts'),

    # API urls
    path('api/products/', ProductListAPIView.as_view(), name='product-list'),
    path('api/categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('api/cart/', CartAPIView.as_view(), name='cart-list'),
    path('api/addtocart/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('api/product/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/category/<str:name>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('api/search/', SearchProductsAPIView.as_view(), name='search-products'),
    path('api/remove/fromcart/', RemoveFromCartAPIView.as_view(), name='delete-from-cart'),
    #path('api/update/cartitem/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
    #path('api/clear/cart/', ClearCartAPIView.as_view(), name='clear-cart'),
    path('api/checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('api/addtocheckout/', AddToCheckoutAPIView.as_view(), name='add-to-checkout'),
    #path('api/wishlist/', WishListAPIView.as_view(), name='wishlist'),
    path('api/addtowishlist/', AddToWishListAPIView.as_view(), name='add-to-wishlist'),
    path('api/remove/fromwishlist/', RemoveFromWishListAPIView.as_view(), name='remove-from-wishlist'),

    path('success/', stk_push_success, name='success'),
]