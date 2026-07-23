from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='my_orders'),
    path('dashboard/', views.dashboard, name='customer_dashboard'),
    
    # AI Endpoints
    path('ai/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('ai/alternatives/', views.alternatives_api, name='alternatives_api'),
]
