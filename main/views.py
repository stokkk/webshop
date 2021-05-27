from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

from operator import attrgetter
from .services import ServiceMain

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from account.models import Order, Cart

from main.utils import calcTotalPrice, next_url_after_login


# Create your views here.

app_name = 'main'

def get_first_photo(product):
    photo = product.productphoto_set.first()
    if photo:
        photo = { 
            'url': photo.photo.photo.url,
            'title': photo.photo.title
        }
    return photo

def index(request):
    products = Variation.objects.filter()[:6]
    top_category = Categories.objects.get(slug='cross')
    context = {
        'products': [
            {
                'id': product.id,
                'name': product.product.name,
                'brand': product.product.brand.name,
                'photo': get_first_photo(product),
                'price': product.reg_price,
                'sale': product.sale_size,
                'new_price': calcTotalPrice(product.reg_price, product.sale_size, 1)
            }
            for product in products
        ], 
        'user': request.user,
        'topcategory': {
            'url': ...,
            'title': '#кроссовки',
            'img': top_category.photo.photo.url
        }
    }
    return render(request, 'main/index.html', context)


def product_detail(request, pk):
    message_success = "Товар успешно добвлен в корзину."
    message_failure = "На складе нету нужного количества товара."
    print(request.POST)
    context = ServiceMain.product_detail_context(request, pk=pk)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                next_url_after_login('product_detail', pk)
            )
        number = int(request.POST['number'])
        product = Variation.objects.get(pk=request.POST['pk'])
        option = get_object_or_404(Options, pk=request.POST['option_id'])
        if option.count < number:
            context.update( {'message_failure': message_failure })
            return render(request, 'main/product_detail.html', context=context)
        try:
            cart_item = Cart.objects.get(       # если будет более одного дубликата
                user=request.user,              # выдаст MultiplyObjectsReturned
                product=product,
                option=option
            )
            if cart_item.count + number > option.count:
                context.update( {'message_failure': message_failure })
                return render(request, 'main/product_detail.html', context=context)
            cart_item.count += number
            cart_item.save()
        except Cart.DoesNotExist:
            cart_item = Cart.objects.create(
                user=request.user,
                product=product,
                count=number,
                option=option
            )
        context.update( {'message_success': message_success })
        return render(request, 'main/product_detail.html', context)    
    return render(request, 'main/product_detail.html', context)


