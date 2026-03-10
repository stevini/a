"""
API Views for the web application.
Provides REST API endpoints for all major functionality.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Category, Products, Cart, WishList, Checkout, User, DefaultImages
from .serializers import ProductSerializer, CategorySerializer
from web.utils.util import get_jwt_token


class CartAPIView(APIView):
    """Get user's cart items."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        products = cart.product.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data})


class TokenProxyView(APIView):
    """Exchange credentials for JWT token."""
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        token_data = get_jwt_token(username, password)

        if "error" in token_data:
            return Response(token_data, status=502)

        return Response(token_data)


class ProductListAPIView(APIView):
    """Get all products."""
    
    def get(self, request):
        products = Products.objects.all()[:50]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    """Get single product by name."""
    
    def get(self, request, name):
        product = get_object_or_404(Products, name=name)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryListAPIView(APIView):
    """Get all categories."""
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailAPIView(APIView):
    """Get single category and its products."""
    
    def get(self, request, name):
        category = get_object_or_404(Category, name=name)
        products = Products.objects.filter(category=category)
        
        category_serializer = CategorySerializer(category)
        products_serializer = ProductSerializer(products, many=True)
        
        return Response({
            'category': category_serializer.data,
            'products': products_serializer.data
        })


class SearchProductsAPIView(APIView):
    """Search products by name."""
    
    def get(self, request):
        search_term = request.query_params.get('q', '')
        if not search_term:
            return Response({'error': 'Query parameter "q" required'}, status=400)
        
        products = Products.objects.filter(name__icontains=search_term)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class AddToCartAPIView(APIView):
    """Add product to cart."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_name = request.data.get('product_name')
        if not product_name:
            return Response({'error': 'product_name required'}, status=400)
        
        product = get_object_or_404(Products, name=product_name)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if product in cart.product.all():
            return Response({'message': 'Product already in cart'}, status=400)
        
        cart.product.add(product)
        cart.save()
        return Response({'message': f'{product} added to cart'})


class RemoveFromCartAPIView(APIView):
    """Remove product from cart."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_name = request.data.get('product_name')
        if not product_name:
            return Response({'error': 'product_name required'}, status=400)
        
        product = get_object_or_404(Products, name=product_name)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if product not in cart.product.all():
            return Response({'message': 'Product not in cart'}, status=400)
        
        cart.product.remove(product)
        cart.save()
        return Response({'message': f'{product} removed from cart'})


class WishListAPIView(APIView):
    """Get user's wishlist items."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        wishlist, _ = WishList.objects.get_or_create(user=request.user)
        products = wishlist.product.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data})


class AddToWishListAPIView(APIView):
    """Add product to wishlist."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_name = request.data.get('product_name')
        if not product_name:
            return Response({'error': 'product_name required'}, status=400)
        
        product = get_object_or_404(Products, name=product_name)
        wishlist, _ = WishList.objects.get_or_create(user=request.user)
        
        if product in wishlist.product.all():
            return Response({'message': 'Product already in wishlist'}, status=400)
        
        wishlist.product.add(product)
        wishlist.save()
        return Response({'message': f'{product} added to wishlist'})


class RemoveFromWishListAPIView(APIView):
    """Remove product from wishlist."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_name = request.data.get('product_name')
        if not product_name:
            return Response({'error': 'product_name required'}, status=400)
        
        product = get_object_or_404(Products, name=product_name)
        wishlist, _ = WishList.objects.get_or_create(user=request.user)
        
        if product not in wishlist.product.all():
            return Response({'message': 'Product not in wishlist'}, status=400)
        
        wishlist.product.remove(product)
        wishlist.save()
        return Response({'message': f'{product} removed from wishlist'})


class CheckoutAPIView(APIView):
    """Get checkout items."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        checkout, _ = Checkout.objects.get_or_create(user=request.user)
        products = checkout.product.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data})


class AddToCheckoutAPIView(APIView):
    """Move cart items to checkout."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        checkout, _ = Checkout.objects.get_or_create(user=request.user)
        
        cart_products = list(cart.product.all())
        checkout.product.add(*cart_products)
        cart.product.remove(*cart_products)
        
        cart.save()
        checkout.save()
        
        return Response({'message': 'Products moved to checkout'})
