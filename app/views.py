from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage, Category, SubCategory
from django.db.models import Q
from .forms import ProductForm, ProductImageForm
from django.contrib import messages

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

def index(request):
  return render(request, 'index.html')


def about_us(request):
  return render(request, 'about_us.html')


def jitender_gupta(request):
  return render(request, 'jitender_gupta.html')


def leadership(request):
  return render(request, 'leadership.html')


# def contact(request):
#   return render(request, 'contact.html')
  
def contact(request):
  if request.method == 'POST':
    name = request.POST.get('username')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
      
    full_message = f""" You have received a new message from Allieva Pharma Contact Form.
      Name: {name}
      Email: {email}
      Phone: {phone}
      Subject: {subject}
      Message:{message}"""
      
    try:
      send_mail(
        subject=f"New Contact Form Submission: {subject}",
        message=full_message,
        from_email=None,  # Will use DEFAULT_FROM_EMAIL
        recipient_list=['info@allievapharma.com'],
        fail_silently=False,
        )
      messages.success(request, 'Your message has been sent successfully!')
    except BadHeaderError:
      return HttpResponse('Invalid header found.')
    return redirect('contact')
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


def category_products(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {
        "category": category,
        "products": products
    })


def subcategory_products(request, category_name, subcategory_name):
  category = get_object_or_404(Category, name__iexact=category_name)
  subcategory = get_object_or_404(SubCategory, name__iexact=subcategory_name, category=category)
  products = Product.objects.filter(category=category, subcategory=subcategory)
  return render(request, 'subcategory_products.html', {
    "category": category,
    "subcategory": subcategory,
    "products": products
  })


def search_products(request):
    query = request.GET.get('q', '')
    products = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand_name__icontains=query) |
            Q(composition__icontains=query) |
            Q(descriptions__icontains=query) |
            Q(uses__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'products': products
    }
    return render(request, 'search.html', context)
