from django.contrib import admin
from .models import Category, Product, ProductImage, Review

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('parent',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = False

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_price_admin', 'category', 'availability', 'created_at')
    list_filter = ('category', 'availability', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline, ReviewInline]
    list_editable = ('availability',)
    
    def formatted_price_admin(self, obj):
        return f"{obj.price} ر.س"
    formatted_price_admin.short_description = 'السعر (ريال)'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
