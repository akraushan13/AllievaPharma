from django.shortcuts import render, redirect

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


def shop(request):
    return render(request, 'shop.html')


def shop_single(request):
    return render(request, 'shop_single.html')