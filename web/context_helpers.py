"""
Helper functions to build context data for views.
Centralizes data dictionary creation to avoid global state issues.
"""
from django.db.models import Count
from .models import Category, Products, Cart, DefaultImages
from .forms import AddToCart


def get_base_context(request):
    """
    Build base context dictionary for all views.
    
    Args:
        request: Django request object
        
    Returns:
        dict: Context dictionary with common data
    """
    # Only get/create cart for authenticated users
    cart = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    
    context = {
        "cart": cart,
        "products": Products.objects.all()[:4],
        "active_products": Products.objects.filter(active=True),
        "categories": Category.objects.all(),
        "categories_featured": Category.objects.all()[:6],
        "countable_categories": Category.objects.annotate(count=Count('product')),
        "default_image": DefaultImages.objects.first(),
        "global_add_form": AddToCart(request.GET)
    }
    return context


def get_cart_products(request):
    """
    Get products in user's cart.
    
    Args:
        request: Django request object
        
    Returns:
        QuerySet: Products in cart, or None if not authenticated
    """
    if not request.user.is_authenticated:
        return None
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return cart


def get_category_products(category_queryset):
    """
    Build dictionary mapping categories to their products.
    
    Args:
        category_queryset: QuerySet of Category objects with count annotation
        
    Returns:
        dict: {category: products_queryset}
    """
    result = {}
    for category in category_queryset:
        result[category] = category.product.all()
    return result
