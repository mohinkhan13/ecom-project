# myapp/context_processors.py

from .models import Category  # or any model you want to pass

def common_data(request):
    categories = Category.objects.all()  # Example: Fetch all categories
    return {
        'categories': categories,  # This will be available in all templates
    }
