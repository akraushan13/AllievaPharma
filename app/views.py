import smtplib, os, random

from .models import Product, ProductImage, Category, SubCategory, JobPosting, NewsEvent
from .forms import ProductForm, ProductImageForm, ApplicationForm
from .utils import send_email, get_product_by_code

from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.utils.html import escape
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


def error_403(request, exception=None):
	return render(request, "errors/403.html", status=403)


def error_404(request, exception=None):
	return render(request, "errors/404.html", status=404)


def error_500(request):
	return render(request, "errors/500.html", status=500)


def contact(request):
	if request.method == 'POST':
		name = request.POST.get('username')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		
		# Build HTML email body
		full_message = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="border:1px solid #ddd; border-radius:8px; padding:20px; max-width:600px; margin:auto;">
              <h2 style="color:#1B00A0;">📩 New Contact Form Submission</h2>
              <p><b>Name:</b> {name}</p>
              <p><b>Email:</b> {email}</p>
              <p><b>Phone:</b> {phone}</p>
              <p><b>Subject:</b> {subject}</p>
              <hr>
              <p><b>Message:</b></p>
              <p>{message}</p>
              <hr>
              <p style="font-size:12px; color:#777;">
                This message was sent from the <a href="{request.build_absolute_uri(reverse('contact'))}">Allieva Pharma Contact Page</a>.
              </p>
            </div>
          </body>
        </html>
        """
		
		success, response_msg = send_email(
			subject=f"New Contact Form Submission: {subject}",
			body_html=full_message  # your utils.py expects body_html
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


def show_all_product(request):
	products = Product.objects.all().distinct().order_by('-id')
	
	paginator = Paginator(products, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {"page_obj": page_obj}
	return render(request, 'products.html', context)


def product_detail(request, product_slug):
	product = get_object_or_404(Product, slug=product_slug)
	images = product.images.all()
	product_url = request.build_absolute_uri(product.get_absolute_url())
	
	return render(request, 'productDetail.html', {"product": product, "images": images, "product_url": product_url, 'hide_whatsapp': True, })


def category_products(request, category_name):
	category = get_object_or_404(Category, name__iexact=category_name)
	products = Product.objects.filter(category=category).distinct().order_by('-id')
	
	paginator = Paginator(products, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	return render(request, 'category_products.html', {
		"category": category,
		"page_obj": page_obj
	})


def subcategory_products(request, category_name, subcategory_name):
	category = get_object_or_404(Category, name__iexact=category_name)
	subcategory = get_object_or_404(SubCategory, name__iexact=subcategory_name, category=category)
	products = Product.objects.filter(category=category, subcategory=subcategory).distinct().order_by('-id')
	
	paginator = Paginator(products, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	return render(request, 'subcategory_products.html', {
		"category": category,
		"subcategory": subcategory,
		"page_obj": page_obj
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
			Q(uses__icontains=query) |
			Q(subcategory__name__icontains=query) |
			Q(category__name__icontains=query)
		).distinct().order_by('-id')
	
	paginator = Paginator(products, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	context = {
		'query': query,
		'page_obj': page_obj
	}
	return render(request, 'search.html', context)


def download_catalogue(request):
	# Path to your file in static folder
	file_path = os.path.join(settings.STATIC_DIR, 'catalogue', 'Products-LBL-All.pdf')
	
	if not os.path.exists(file_path):
		raise Http404("Catalogue not found.")
	
	# FileResponse streams the file without loading it entirely into memory
	return FileResponse(open(file_path, 'rb'), as_attachment=False, filename='Products-LBL-All.pdf')


# def send_enquiry(request):
# 	if request.method == 'POST':
# 		first_name = request.POST.get('first_name')
# 		last_name = request.POST.get('last_name')
# 		email = request.POST.get('email')
# 		phone = request.POST.get('phone')
# 		subject = request.POST.get('subject')
# 		message = request.POST.get('message')
# 		product = request.POST.get('product')
# 		slug = request.POST.get('product_slug')
# 		# image_url = request.POST.get('product_image')
#
# 		# Generate full product URL
# 		product_url = request.build_absolute_uri(reverse("productDetail", args=[slug]))
#
# 		# Build HTML email body
# 		full_message = f"""
#         <html>
#         <body style="font-family: Arial, sans-serif; line-height: 1.6;">
#           <h2 style="color:#007bff;">📩 New Product Enquiry - Allieva Pharma</h2>
#           <hr>
#           <h3>🔹 Product Details</h3>
#           <p><strong>{escape(product)}</strong></p>
#           <p><a href="{product_url}" target="_blank">{product_url}</a></p>
#
#
#           <h3>👤 Customer Details</h3>
#           <p><strong>Name:</strong> {escape(first_name)} {escape(last_name)}<br>
#              <strong>Email:</strong> {escape(email)}<br>
#              <strong>Phone:</strong> {escape(phone)}</p>
#
#           <h3>📝 Enquiry</h3>
#           <p><strong>Subject:</strong> {escape(subject)}<br>
#              <strong>Message:</strong><br>{escape(message)}</p>
#
#           <hr>
#           <p style="font-size:12px; color:#888;">This enquiry was sent from the Allieva Pharma website.</p>
#         </body>
#         </html>
#         """
#
# 		success, response_msg = send_email(
# 			subject=f"New Product Enquiry: {subject or product}",
# 			body_html=full_message,
# 			# image_url=image_url  # pass for inline image
# 		)
#
# 		if success:
# 			previous_page = request.META.get("HTTP_REFERER", reverse("products"))
# 			return render(request, "thankyou.html", {
# 				"message": "Your enquiry has been sent successfully!",
# 				"previous_page": previous_page
# 			})
# 		else:
# 			messages.error(request, response_msg)
# 			return redirect("products")
#
# 	return redirect("products")


def send_enquiry(request):
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		product = request.POST.get('product')
		slug = request.POST.get('product_slug')
		collaboration_type = request.POST.get('collaboration_type')
		
		# Generate full product URL
		if slug:
			try:
				product_url = request.build_absolute_uri(reverse("productDetail" , args=[slug]))
			except Exception:
				product_url = request.build_absolute_uri(reverse("products"))
		else:
			product_url = request.build_absolute_uri(reverse("products"))
		
		# Build HTML email body
		full_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
          <h2 style="color:#007bff;">📩 New Product Enquiry - Allieva Pharma</h2>
          <hr>
          <h3>🔹 Product Details</h3>
          <p><strong>{escape(product)}</strong></p>
          <p><a href="{product_url}" target="_blank">{product_url}</a></p>

          <h3>👤 Customer Details</h3>
          <p><strong>Name:</strong> {escape(first_name)} {escape(last_name)}<br>
             <strong>Email:</strong> {escape(email)}<br>
             <strong>Phone:</strong> {escape(phone)}</p>

          <h3>📝 Enquiry</h3>
          <p><strong>Subject:</strong> {escape(subject)}<br>
             <strong>Message:</strong><br>{escape(message)}</p>

          <p><strong>Collaboration Type:</strong> {collaboration_type}</p>

          <hr>
          <p style="font-size:12px; color:#888;">This enquiry was sent from the Allieva Pharma website.</p>
        </body>
        </html>
        """
		
		# Choose recipient email based on collaboration type
		if collaboration_type == "international":
			recipient_email = "export@allievapharma.com"
		else:
			recipient_email = "info@allievapharma.com"
		
		success , response_msg = send_email(
			subject=f"New Product Enquiry: {subject or product}" ,
			body_html=full_message ,
			to_email=recipient_email ,  # override based on selection
		)
		
		if success:
			previous_page = request.META.get("HTTP_REFERER" , reverse("products"))
			return render(request , "thankyou.html" , {
				"message": "Your enquiry has been sent successfully!" ,
				"previous_page": previous_page
			})
		else:
			messages.error(request , response_msg)
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
	jobs = JobPosting.objects.all()
	if request.method == "POST":
		form = ApplicationForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect("career")
	else:
		form = ApplicationForm()
	context = {"jobs": jobs, "form": form}
	return render(request, 'career.html', context)


def news_event(request):
	# newsEvent = NewsEvent.objects.all()
	newsEvent = NewsEvent.objects.all().order_by('-id')
	
	paginator = Paginator(newsEvent, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {"page_obj": page_obj}
	return render(request, 'news_blog.html', context)


def news_detail(request, pk):
	news_item = get_object_or_404(NewsEvent, id=pk)
	recent_news = NewsEvent.objects.exclude(id=pk).order_by('-id')[:5]
	context = {"news_item": news_item,
	           "recent_news": recent_news
	           }
	return render(request, "news_detail.html", context)
