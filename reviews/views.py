from reviews.models import Review  # 👈 Добавить импорт

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(request, "catalog/product_detail.html", {
        "product": product,
        "reviews": reviews,
    })
