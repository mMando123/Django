from .models import Category

def categories_processor(request):
    """Add categories to the template context for the navigation menu."""
    return {
        'categories': Category.objects.filter(parent=None),
    }
