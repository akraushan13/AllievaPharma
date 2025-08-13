import smtplib, os


from .models import Product, ProductImage, Category, SubCategory
from .forms import ProductForm, ProductImageForm

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect



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

    full_message =f"""You have received a new message from Allieva Pharma Contact Form.
                  Name: {name}
                  Email: {email}
                  Phone: {phone}
                  Subject: {subject}
                  Message: {message}"""

    # SMTP settings
    SMTP_SERVER = "mail.allievapharma.com"
    SMTP_PORT = 465
    USERNAME = "info@allievapharma.com"
    PASSWORD = "Allieva@0908"
    FROM_EMAIL = USERNAME
    TO_EMAIL = "info@allievapharma.com"

    try:
      print("Connecting to SMTP server...")
      server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
      server.login(USERNAME.strip(), PASSWORD)
      print(" Login successful!")
      # Prepare email with subject + body
      email_content = f"Subject: New Contact Form Submission: {subject}\n\n{full_message}"
      # Send email
      server.sendmail(FROM_EMAIL, TO_EMAIL, email_content)
      print("✅ Email sent successfully!")
      server.quit()
      messages.success(request, 'Your message has been sent successfully!')
    except smtplib.SMTPAuthenticationError as e:
      print("❌ Authentication failed:", e)
      messages.error(request, 'Email authentication failed. Please check credentials.')
    except smtplib.SMTPConnectError as e:
      print("❌ Connection failed:", e)
      messages.error(request, 'Could not connect to email server.')
    except Exception as e:
      print("❌ Error:", e)
      messages.error(request, f"An unexpected error occurred: {e}")
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


def download_catalogue(request):
  # Path to your file in static folder
  file_path = os.path.join(settings.STATIC_DIR, 'catalogue', 'Products-LBL-All.pdf')
  
  if not os.path.exists(file_path):
    raise Http404("Catalogue not found.")
  
  # FileResponse streams the file without loading it entirely into memory
  return FileResponse(open(file_path, 'rb'), as_attachment=False, filename='Products-LBL-All.pdf')