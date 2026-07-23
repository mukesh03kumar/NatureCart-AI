from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Seller', 'Seller'),
        ('Customer', 'Customer'),
    )
    
    PREFERENCE_CHOICES = (
        ('Zero-Waste', 'Zero Waste Focus'),
        ('Organic', 'Organic & Natural'),
        ('Plastic-Free', '100% Plastic Free'),
        ('Carbon-Footprint', 'Carbon Footprint Minimizer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    # User's eco preferences
    preference = models.CharField(
        max_length=50, 
        choices=PREFERENCE_CHOICES, 
        blank=True, 
        null=True
    )
    
    # Dynamic aggregate stats
    total_plastic_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_co2_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_premium_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Seller_app.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.customer.username} - {self.product.name} ({self.quantity})"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Impact for this specific order
    plastic_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    co2_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Seller_app.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name if self.product else 'Deleted Product'} x {self.quantity}"


class PlasticAlternative(models.Model):
    plastic_product_name = models.CharField(
        max_length=100, 
        help_text="Name of the harmful plastic item (e.g., Plastic Toothbrush)"
    )
    alternative_product = models.ForeignKey(
        'Seller_app.Product', 
        on_delete=models.CASCADE,
        help_text="The green alternative sold on NatureCart"
    )
    co2_savings = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="CO2 savings per unit in kg"
    )
    plastic_savings = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Plastic saved per unit in kg"
    )
    reasoning = models.TextField(
        help_text="AI reasoning explaining why this is better"
    )

    def __str__(self):
        return f"{self.plastic_product_name} -> {self.alternative_product.name}"
