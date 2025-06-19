from catalog.models import Category


def category_list(request):
    return {
        'categories': Category.objects.exclude(name__iexact='Home').exclude(slug__iexact='home')
    }
