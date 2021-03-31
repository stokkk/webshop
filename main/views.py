from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, ProductPhoto
# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'main/index.html', context)