from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('Bags', 'Reusable Bags'),
        ('Dental', 'Dental Care'),
        ('Hydration', 'Hydration & Straws'),
        ('Composting', 'Composting & Kitchen'),
        ('Cleaning', 'Natural Cleaning'),
        ('Stationery', 'Seed Paper & Stationery'),
        ('Home', 'Eco Home & Candles'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)
    
    # Eco impact values
    plastic_saving_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Plastic saved in kg per unit compared to plastic equivalent"
    )
    co2_saving_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="CO2 saved in kg per unit compared to plastic equivalent"
    )
    
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"
