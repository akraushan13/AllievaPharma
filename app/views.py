from django.shortcuts import render, redirect
from .models import Product,ProductImage
from .forms import ProductForm, ProductImageForm
from django.contrib import messages
# Create your views here.

def index(request):
  return render(request, 'index.html')


def about_us(request):
  return render(request, 'about_us.html')


def jitender_gupta(request):
  return render(request, 'jitender_gupta.html')


def leadership(request):
  return render(request, 'leadership.html')


def contact(request):
  return render(request, 'contact.html')
  
  
def medicine_verification(request):
  return render(request, 'medicine-verification.html')


# def shop(request):
#   return render(request, 'products.html')


# def shop_single(request):
#   return render(request, 'productDetail.html')


# def create_product(request):
#   productform = ProductForm()
#   productimageform = ProductImageForm()
#
#   if request.method == 'POST':
#
#     files = request.FILES.getlist('images')
#
#     productform = ProductForm(request.POST, request.FILES)
#     if productform.is_valid():
#       product = productform.save(commit=False)
#       product.vendor = request.user
#       product.save()
#       messages.success(request, "Product created successfully")
#
#       for file in files:
#         ProductImage.objects.create(product=product, images=file)
#
#       return redirect("/")
#
#   context = {"p_form": productform, "i_form": productimageform}
#   return render(request, "create.html", context)
 
  
def show_all_product(request):
  products = Product.objects.all()
  context = {"products": products}
  return render(request, 'products.html', context)
  
def product_detail(request, pk):
  product = Product.objects.get(id=pk)
  images = ProductImage.objects.filter(product=product)
  context = {"product": product, "images": images}
  return render(request, 'productDetail.html', context)