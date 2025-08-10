
from django.urls import path

from . import views

urlpatterns = [


    # Store main page

    path('', views.store, name='store'),


    # Individual product

    path('product/<slug:product_slug>/', views.product_info, name='product-info'),


    # Search

    path('search/', views.search, name='search'),


    # Individual category

    path('category/<slug:category_slug>/', views.list_category, name='list-category'),


]














