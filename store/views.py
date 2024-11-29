from django.shortcuts import render

def home(request):
    return render(request, "store/pages/home.html")

def products(request):
    return render(request, "store/pages/products.html")
    