from django.db import models

# Create your models here.


class Product(models.Model):
  product_id = models.AutoField(primary_key=True)
  product_name = models.CharField(max_length=100)
  brand_name = models.CharField(max_length=100)
  composition = models.CharField(max_length=100)
  manufacture  = models.CharField(max_length=100, default="Allieva Pharma Private Limited")
  form  = models.CharField(max_length=100, default="")
  country_of_origin = models.CharField(max_length=50, default="India")
  packing  = models.CharField(max_length=100, default="")
  category = models.CharField(max_length=100, default="")
  subcategory = models.CharField(max_length=50, default="")
  # price = models.IntegerField(default=0)
  descriptions = models.TextField()
  uses = models.TextField()
  side_effects = models.TextField()
  dosage = models.TextField()
  
  def save(self, *args, **kwargs):
    if not self.composition:
      self.composition = self.product_name
    super().save(*args, **kwargs)
  
  def __str__(self):
    return self.product_name
  
class ProductImage(models.Model):
  objects = None
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
  images = models.ImageField(upload_to='images')
  
