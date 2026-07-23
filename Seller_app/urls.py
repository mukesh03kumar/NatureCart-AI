from django.urls import path
from . import views

urlpatterns = [
    path('seller/', views.dashboard, name='seller_dashboard'),
    path('seller/products/', views.my_products, name='my_products'),
    path('seller/products/add/', views.add_product, name='add_product'),
    path('seller/products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('seller/products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('seller/orders/', views.manage_orders, name='manage_orders'),
    path('seller/orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
