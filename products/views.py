from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer
from .forms import ProductForm
from accounts.models import UserProfile
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Category.objects.all()
        if self.action == 'list':
            # Only return parent categories in the main list
            queryset = queryset.filter(parent=None)
        return queryset

    @action(detail=False)
    def featured(self, request):
        featured = Category.objects.filter(featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['created_at', 'price', 'average_rating']

    @action(detail=False)
    def featured(self, request):
        featured = self.get_queryset().filter(featured=True)
        page = self.paginate_queryset(featured)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def trending(self, request):
        trending = self.get_queryset().filter(trending=True)
        page = self.paginate_queryset(trending)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(trending, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def by_category(self, request):
        category_slug = request.query_params.get('category', None)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = self.get_queryset().filter(category=category)
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter is required'}, status=400)

# Template Views
def category_list(request):
    categories = Category.objects.filter(parent=None)
    featured_categories = Category.objects.filter(featured=True)
    context = {
        'categories': categories,
        'featured_categories': featured_categories,
    }
    return render(request, 'products/categories.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    
    # Check if user is an expert
    is_expert = False
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            is_expert = profile.role == 'expert_user'
        except UserProfile.DoesNotExist:
            pass
    
    context = {
        'category': category,
        'products': products,
        'is_expert': is_expert,
    }
    return render(request, 'products/category_detail.html', context)

@login_required
def add_product(request, category_slug):
    # Check if user is an expert
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'expert_user':
            raise PermissionDenied("Only expert users can add products.")
    except UserProfile.DoesNotExist:
        raise PermissionDenied("User profile not found.")
    
    category = get_object_or_404(Category, slug=category_slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.added_by = request.user
            product.save()
            messages.success(request, 'تم إضافة المنتج بنجاح!')
            return redirect('products:category_detail', slug=category_slug)
    else:
        form = ProductForm()
    
    return render(request, 'products/add_product.html', {
        'form': form,
        'category': category
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by('-created_at')
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'تم إضافة تقييمك بنجاح!')
        else:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
            
    return redirect('products:product_detail', slug=slug)

def home(request):
    all_products = Product.objects.all()[:6]  # Get all products, limit to 6
    categories = Category.objects.filter(parent=None)[:6]
    
    context = {
        'featured_products': all_products,  # Use all products as featured
        'categories': categories,
    }
    return render(request, 'home.html', context)

def compare_products(request):
    comparison_list = request.session.get('comparison_list', [])
    products = Product.objects.filter(id__in=comparison_list)
    
    # Get all unique specification keys
    all_specifications = set()
    has_specifications = False
    
    # Convert specifications from string to dict if needed
    for product in products:
        if product.specifications:
            has_specifications = True
            if isinstance(product.specifications, str):
                try:
                    product.specifications = eval(product.specifications)
                except:
                    product.specifications = {}
            all_specifications.update(product.specifications.keys())
    
    all_specifications = sorted(all_specifications)
    
    context = {
        'products': products,
        'has_specifications': has_specifications,
        'all_specifications': all_specifications,
    }
    return render(request, 'products/compare.html', context)

@require_POST
def add_to_compare(request, product_id):
    comparison_list = request.session.get('comparison_list', [])
    
    # Limit to 4 products
    if len(comparison_list) >= 4:
        return JsonResponse({
            'status': 'error',
            'message': 'يمكنك مقارنة 4 منتجات كحد أقصى'
        }, status=400)
    
    if product_id not in comparison_list:
        comparison_list.append(product_id)
        request.session['comparison_list'] = comparison_list
        return JsonResponse({
            'status': 'success',
            'message': 'تمت إضافة المنتج للمقارنة',
            'count': len(comparison_list)
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'المنتج موجود بالفعل في قائمة المقارنة'
    }, status=400)

@require_POST
def remove_from_compare(request, product_id):
    comparison_list = request.session.get('comparison_list', [])
    if product_id in comparison_list:
        comparison_list.remove(product_id)
        request.session['comparison_list'] = comparison_list
    return JsonResponse({
        'status': 'success',
        'message': 'تم إزالة المنتج من المقارنة',
        'count': len(comparison_list)
    })

def clear_comparison(request):
    if 'comparison_list' in request.session:
        del request.session['comparison_list']
    return redirect('products:category_list')

def comparison_processor(request):
    comparison_list = request.session.get('comparison_list', [])
    products = Product.objects.filter(id__in=comparison_list) if comparison_list else []
    
    # Convert any non-ASCII strings to unicode
    products_list = []
    for product in products:
        product.name = str(product.name)
        product.description = str(product.description) if product.description else ''
        products_list.append(product)
    
    return {
        'comparison_list': products_list,
        'comparison_count': len(products_list)
    }
