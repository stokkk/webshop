from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LogInForm, RegisterForm

from django.contrib.auth.models import User
from operator import attrgetter, itemgetter

import logging

logger = logging.getLogger(__name__)

#models
from .models import Cart, Order
from main.models import Variation, ProductPhoto, Product, Photo
from main.utils import calcTotalPrice

@login_required(login_url="/account/login")
def AccountView(request):
    return render(request, 'account/account.html', context={'user': request.user})


@login_required(login_url="/account/login")
def CartView(request):
    if request.method == "POST" and "remove" in request.POST: 
        product_id = int(request.POST['remove'])
        option_id = int(request.POST['option_id'])
        try:
            delete_item = Cart.objects.get(
                user=request.user,
                product_id=product_id,
                option_id=option_id
            )
            delete_item.delete()
        except Cart.DoesNotExist:
            logger.warning("No have cart item with product id '%s'" % str(product_id))
    cart_items = get_cart_items(request)
    return render(request, "account/cart.html", context={
        'user': request.user,
        'cart_items': cart_items,
        'total': round(sum(map(itemgetter('totalPrice'), cart_items)), 2),
        'xhr_url': reverse('cart_count')
    })


def LogInView(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        next_page_url = request.GET['next']
        if form.is_valid():
            client_data = form.cleaned_data
            user = authenticate(username=client_data['login'],
            password=client_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next_page_url)
        return render(request, 'account/login.html', context={     # В случае если форма не верна.
            'user': request.user,
            'form': form,
        })
    form = LogInForm()
    return render(request, 'account/login.html', context={      # Первичное отображение формы.
        'user': request.user,
        'form': form
    })


def LogOutView(request):
    logout(request)
    return HttpResponseRedirect("/")


def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # может быть проверка существования юзера в базе.
            # или она может быть в методе clean формы RegisterForm
            client_data = form.cleaned_data
            user = User(
                username=client_data['login'],
                email=client_data['email'],
                password=client_data['password']
            )

            user.save()
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'account/registration.html', context={
            'user': request.user,
            'form': form})
    
    form = RegisterForm()
    return render(request, 'account/registration.html', context={
        'user': request.user,
        'form': form})

    
def CartCountView(request):
    if request.method == 'GET':
        print(request.GET)
        cart_id = int(request.GET.get('cart_id'))
        cart_count = int(request.GET.get('cart_count'))
        option_id = int(request.GET.get('option_id'))
        cart = get_object_or_404(
            Cart,
            product_id=cart_id,
            user_id=request.user.pk,
            option_id=option_id
        )
        if cart.option.count >= cart_count:
            cart.count = cart_count
            cart.save()
        logger.warn("User {0} update count product {1} ({2})".format(
            cart.user.username,
            cart.product.product.name,
            cart.count
        ))
    user_products = Cart.objects.filter(user_id=cart.user.id)
    return JsonResponse({
        'totalItemPrice': calcTotalPrice(
            cart.product.reg_price,
            cart.product.sale_size,
            cart.count
        ),
        'totalPrice': round(sum(
            map(
                lambda inst: calcTotalPrice(*inst),
                zip(
                    map(attrgetter('product.reg_price'), user_products),
                    map(attrgetter('product.sale_size'), user_products),
                    map(attrgetter('count'), user_products)
                )
            )
        ), 2),
        'count': cart.count
    })


def get_cart_items(request):
    return [
        {
            'product': {
                'id': item.product.id,
                'sku': item.product.sku,
                'name': item.product.product.name,
                'brand': item.product.product.brand.name,
                'price': item.product.reg_price,
                'sale': item.product.sale_size,
                'count': item.option.count,
                'size': {'id': item.option.id, 'value':item.option.size},
                'color': item.product.color.name,
                'photo': ProductPhoto.objects.filter(product=item.product).first().photo.photo
            },
            'number': item.count,
            'totalPrice': calcTotalPrice(
                item.product.reg_price,
                item.product.sale_size,
                item.count
            )
        } for item in Cart.objects.filter(user=request.user)
    ]