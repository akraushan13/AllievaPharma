from django.urls import path
from . import views


urlpatterns = [
  path('',views.index, name='index'),
  path('about-us/',views.about_us, name='about_us'),
  path('jitender-gupta/',views.jitender_gupta, name='jitender_gupta'),
  path('leadership/',views.leadership, name='leadership'),
  path('contact/',views.contact, name='contact'),
  path('Medicine/verification',views.medicine_verification, name='medicine-verification'),
  
  
  # path("create_product", views.create_product, name='create'),
  path('products/',views.show_all_product, name='products'),
  path('product/<int:pk>/',views.product_detail, name='productDetail'),
]
