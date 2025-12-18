from .models import Category

def categories_menu(request):
    categories = Category.objects.prefetch_related("subcategories").all()
    return {"menu_categories": categories}