from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('<slug:slug>/', views.category_detail, name='category'),
    path('brands/', views.brand_list, name='brands'),

]
