from django.urls import path
from .views import brand_list, products_by_brand, category_detail, search_products, like_product
from . import views

app_name = 'catalog'

urlpatterns = [
    path("brands/", brand_list, name="brand_list"),
    path("brand/<int:brand_id>/", products_by_brand, name="products_by_brand"),
    path("search/", search_products, name="search_products"),  # <-- перемещён выше
    path("<slug:slug>/", category_detail, name="category"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("product/<int:product_id>/like/", like_product, name="like_product"),

]
