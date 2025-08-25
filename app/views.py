import smtplib, os, random

from .models import Product, ProductImage, Category, SubCategory
from .forms import ProductForm, ProductImageForm
from .utils import send_email, get_product_by_code

from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.utils.html import escape



# Create your views here.

def index(request):
  return render(request, 'index.html')


def about_us(request):
  return render(request, 'about_us.html')


def jitender_gupta(request):
  return render(request, 'jitender_gupta.html')


def leadership(request):
  return render(request, 'leadership.html')
  
def thankyou(request):
  return render(request, 'thankyou.html')


# def contact(request):
#   return render(request, 'contact.html')

import smtplib
from django.shortcuts import render, redirect
from django.contrib import messages


def contact(request):
  if request.method == 'POST':
    name = request.POST.get('username')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    
    full_message = f"""
      You have received a new message from Allieva Pharma Contact Form.

      Name: {name}
      Email: {email}
      Phone: {phone}
      Subject: {subject}
      Message: {message}
      """
    
    success, response_msg = send_email(
      subject=f"New Contact Form Submission: {subject}",
      body=full_message
    )
    
    if success:
      return render(request, "thankyou.html", {
        "message": "Your message has been sent successfully!",
        "previous_page": reverse("contact")
      })
    else:
      messages.error(request, response_msg)
      return redirect("contact")
  
  return render(request, 'contact.html')


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


def download_catalogue(request):
  # Path to your file in static folder
  file_path = os.path.join(settings.STATIC_DIR, 'catalogue', 'Products-LBL-All.pdf')
  
  if not os.path.exists(file_path):
    raise Http404("Catalogue not found.")
  
  # FileResponse streams the file without loading it entirely into memory
  return FileResponse(open(file_path, 'rb'), as_attachment=False, filename='Products-LBL-All.pdf')


def send_enquiry(request):
  if request.method == 'POST':
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    product = request.POST.get('product')
    
    full_message = f"""
      You have received a new product enquiry from Allieva Pharma.

      Product: {product}
      Name: {first_name} {last_name}
      Email: {email}
      Subject: {subject}
      Message: {message}
      """
    
    success, response_msg = send_email(
      subject=f"New Product Enquiry: {subject}",
      body=full_message
    )
    
    if success:
      previous_page = request.META.get("HTTP_REFERER", reverse("products"))
      return render(request, "thankyou.html", {
        "message": "Your enquiry has been sent successfully!",
        "previous_page": previous_page
      })
    else:
      messages.error(request, response_msg)
      return redirect("products")
  
  return redirect("products")


CAPTCHA_SESSION_KEY = "medicine_captcha_answer"
def _new_captcha(request):
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    request.session[CAPTCHA_SESSION_KEY] = a + b
    return f"{a} + {b} = ?"


@require_http_methods(["GET", "POST"])
def medicine_verification(request):
  context = {}
  if request.method == "GET":
    # Fresh captcha on first load
    context["captcha_question"] = _new_captcha(request)
    return render(request, "medicine_verification.html", context)
  
  # ----- POST: validate form & captcha -----
  name = (request.POST.get("name") or "").strip()
  email = (request.POST.get("email") or "").strip()
  phone = (request.POST.get("phone") or "").strip()
  country = (request.POST.get("country") or "").strip()
  verification_code = (request.POST.get("verification_code") or "").strip()
  user_captcha = (request.POST.get("captcha-answer") or "").strip()
  
  # Server-side captcha check
  expected = request.session.get(CAPTCHA_SESSION_KEY)
  try:
    user_value = int(user_captcha)
  except (TypeError, ValueError):
    user_value = None
  
  if expected is None or user_value != expected:
    messages.error(request, "Captcha is incorrect. Please try again.")
    # Always issue a new captcha
    context["captcha_question"] = _new_captcha(request)
    return render(request, "medicine_verification.html", context)
  
  # If you want minimal required field checks on the server too:
  if not all([name, email, phone, country, verification_code]):
    messages.error(request, "Please fill all required fields.")
    context["captcha_question"] = _new_captcha(request)
    return render(request, "medicine_verification.html", context)
  
  # ----- Lookup in CSV -----
  product = get_product_by_code(verification_code)
  # print(product)
  if product:
    # Found the code = genuine
    if product.get("has_full_details"):
      # Newer stock: show all the details
      context["message_class"] = "success"
      context["message"] = "✅ Congratulations! Your Product is found Genuine."
      context["product"] = product
    else:
      # Older stock: code genuine, but details not present
      context["message_class"] = "success"
      context["message"] = (
        "✅ Congratulations! Your Product is found Genuine. "
        "However, detailed product info may not be available for some older stock."
      )
      context["product"] = None
  else:
    # Not found = verification failed
    context["message_class"] = "danger"
    context["message"] = (
      "❌ Product Verification Failed. "
      "If the security label is missing/damaged/unreadable, please contact your medicine provider and request a replacement."
    )
    context["product"] = None
  
  # Rotate captcha on every POST outcome (prevents replay)
  context["captcha_question"] = _new_captcha(request)
  return render(request, "medicine_verification.html", context)


def career(request):
  return render(request, 'career.html')
  
  
def news_blog(request):
  return render(request, 'news_blog.html')


def error_403(request, exception=None):
    return render(request, "errors/403.html", status=403)

def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)
