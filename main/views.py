from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *

from operator import attrgetter
# Create your views here.

app_name = 'main'

def index(request):
    products = ProductVar.objects.all()
    context = {'products': products}
    return render(request, 'main/index.html', context)


def product_detail(request, pk):
    product = get_object_or_404(ProductVar, pk=pk)      # Объект товара
    group_products = ProductVar.objects.filter(group_id=product.group_id)
    attrs = map(attrgetter('attribute'),            # атрибуты товара. Класс - Attributes
        AttributeAndCategory.objects.filter(category=product.product.category_id)
    )
    photos = product.productphoto_set.all()
    main_photo, other_photos = (photos[0], photos[1:]) if len(photos) >= 1 else (None, [])
    context = {
        'product': product,
        'category_attributes': attrs,
        'group_products': group_products,
        'main_photo': main_photo,
        'other_photos': other_photos
    }
    return render(request, 'main/product_detail.html', context)