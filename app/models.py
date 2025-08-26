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
	image = models.ImageField(upload_to='images/', default='images/no-image.jpg')
	brand_name = models.CharField(max_length=100)
	composition = models.CharField(max_length=100)
	manufacture  = models.CharField(max_length=100, default="Allieva Pharma Private Limited")
	form  = models.CharField(max_length=100, default="")
	country_of_origin = models.CharField(max_length=50, default="India")
	packing  = models.CharField(max_length=100, default="")

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
	images = models.ImageField(upload_to='images/', default='images/no-image.jpg')
	
	def __str__(self):
		return str(self.product.name)


class JobTag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	
	def __str__(self):
		return self.name

class JobPosting(models.Model):
	title = models.CharField(max_length=200)
	location = models.CharField(max_length=100)
	urgent = models.CharField(max_length=50)
	posted_on = models.DateField(auto_now_add=True)
	job_description = models.TextField()
	responsibilities = models.TextField()
	requirements = models.TextField()
	tags = models.ManyToManyField(JobTag, related_name="jobs")
	
	def __str__(self):
		return self.title

class Application(models.Model):
	job = models.ForeignKey("JobPosting", on_delete=models.CASCADE, related_name="applications")
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	resume = models.FileField(upload_to="resumes/")
	cover_letter = models.TextField(blank=True, null=True)
	consent = models.BooleanField(default=False)
	applied_on = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.first_name} {self.last_name} - {self.job.title}"


class NewsEventCategory(models.Model):
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name

class NewsEvent(models.Model):
	author = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	category = models.ForeignKey(NewsEventCategory, on_delete=models.SET_NULL, null=True, blank=True)
	short_description = models.TextField()
	description = models.TextField()
	image1 = models.ImageField(upload_to='news_images/', blank=True, null=True)
	image2 = models.ImageField(upload_to='news_images/', blank=True, null=True)
	date = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-date']
	
	def __str__(self):
		return self.title
