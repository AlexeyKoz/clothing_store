from django.urls import path
from .views import brand_list, products_by_brand, category_detail

app_name = 'catalog'

urlpatterns = [
    path("brands/", brand_list, name="brand_list"),
    path("brand/<int:brand_id>/", products_by_brand, name="products_by_brand"),
    path("<slug:slug>/", category_detail, name="category"),
]
