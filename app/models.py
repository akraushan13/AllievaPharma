from django.db import models

# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name


class SubCategory(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return f"{self.category.name} > {self.name}"


class Product(models.Model):
  # id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  brand_name = models.CharField(max_length=100)
  composition = models.CharField(max_length=100)
  manufacture  = models.CharField(max_length=100, default="Allieva Pharma Private Limited")
  form  = models.CharField(max_length=100, default="")
  country_of_origin = models.CharField(max_length=50, default="India")
  packing  = models.CharField(max_length=100, default="")
  
  # ✅ Updated: Use ForeignKey for category and subcategory
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
  subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
  
  # price = models.DecimalField(max_digits=10, decimal_places=2)
  descriptions = models.TextField()
  uses = models.TextField()
  side_effects = models.TextField()
  dosage = models.TextField()
  
  
  def __str__(self):
    return self.name
  
class ProductImage(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
  images = models.ImageField(upload_to='images')
  
  def __str__(self):
    return str(self.product.name)
  
