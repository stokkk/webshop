from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, ProductPhoto, Photo, Attributes, Categories,\
AttributeAndCategory, ProductValue, Values
# Create your views here.

def index(request):
    products = Product.objects.all().order_by('brand__name')
    context = {'products': products}
    return render(request, 'main/index.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk) # Объект товара
    attrs = AttributeAndCategory.objects.filter(category=product.category_id)
    attrs = [attr.attribute for attr in attrs] # атрибуты товара. Класс - Attributes
    values = ProductValue.objects.filter(product=product.id) 
    values = [value.value for value in values] # значения атрибутов товара. Класс - Values
    context = {'product': product, 'category_attributes': attrs, 'product_values': values}
    return render(request, 'main/product_detail.html', context)