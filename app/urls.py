from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('about-us',views.about_us, name='about_us'),
    path('jitender-gupta',views.jitender_gupta, name='jitender_gupta'),
    path('leadership',views.leadership, name='leadership'),
    path('contact',views.contact, name='contact'),
    path('shop',views.shop, name='shop'),
]
