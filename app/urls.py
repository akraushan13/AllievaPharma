from django.urls import path
from . import views


urlpatterns = [
  path('',views.index, name='index'),
  path('about-us/',views.about_us, name='about_us'),
  path('jitender-gupta/',views.jitender_gupta, name='jitender_gupta'),
  path('leadership/',views.leadership, name='leadership'),
  path('contact/',views.contact, name='contact'),
  path('thankyou/',views.thankyou, name='thankyou'),
  path('Medicine/verification',views.medicine_verification, name='medicine_verification'),
  
  # path("create_product", views.create_product, name='create'),
  path('products/',views.show_all_product, name='products'),
  path('products/<int:pk>/',views.product_detail, name='productDetail'),
  path('products/category/<str:category_name>/', views.category_products, name='category_products'),
  path('products/category/<str:category_name>/<str:subcategory_name>/', views.subcategory_products,name='subcategory_products'),
  path('search/', views.search_products, name='search_products'),
  path('download-catalogue/', views.download_catalogue, name='download_catalogue'),
  path('send-enquiry/', views.send_enquiry, name='send_enquiry'),

]