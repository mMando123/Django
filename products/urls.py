from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)

app_name = 'products'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Template URLs
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/<slug:category_slug>/add-product/', views.add_product, name='add_product'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/add-review/', views.add_review, name='add_review'),
    path('compare/', views.compare_products, name='compare'),
    path('add-to-compare/<int:product_id>/', views.add_to_compare, name='add_to_compare'),
    path('remove-from-compare/<int:product_id>/', views.remove_from_compare, name='remove_from_compare'),
    path('clear-comparison/', views.clear_comparison, name='clear_comparison'),
]
