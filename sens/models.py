from django.db import models
from products.models import Product

# Create your models here.
class sens(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id = models.IntegerField(max_length=10)
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products"
    )