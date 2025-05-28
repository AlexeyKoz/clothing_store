from django.urls import path
from .views import brand_list, category_detail

app_name = 'catalog'

urlpatterns = [
    path('brands/', brand_list, name='brands'),
    path('<slug:slug>/', category_detail, name='category'),
]
