from django.urls import path
from . import views
from .views import ProductListView


urlpatterns = [
    path('404/', views.view404),
    path('about/', views.about),
    path('cart/', views.cart),
    path('category/', views.category_view),
    path('category/<str:name>/', views.category),
    path('checkout/', views.checkout),
    path('comingsoon/', views.comingSoon),
    path('contact/', views.contact),
    path('dashboard/', views.dashboard),
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
    path('search/', views.search_product, name='search'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('checkouttest/', views.checkout_test, name='checkouttest'),
    path('listproducts/', views.listProducts, name='listproducts'),
    path('disablewithoutpic/', views.disableWoutPic, name='disablewithoutpic'),
    path('api/products/', ProductListView.as_view(), name='product-list'),
]