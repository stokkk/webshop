from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LogInForm, RegisterForm, OrderForm

from django.contrib.auth.models import User
from operator import attrgetter, itemgetter

from main.services.contextmanage import base_context_genre
from .services.accountservice import products_json, create_order, get_cart_items
import logging

logger = logging.getLogger(__name__)

from .models import Cart, Order
from main.models import Variation, ProductPhoto, Options
from main.utils import calcTotalPrice

@login_required(login_url="/account/login")
def AccountView(request):
    context = base_context_genre(request)
    return render(request, 'account/account.html', context=context)


@login_required(login_url="/account/login")
def CartView(request):
    if request.method == "POST" and "remove" in request.POST:
        option_id = int(request.POST['remove'])
        option = Options.objects.get(pk=option_id)
        try:
            delete_item = Cart.objects.get(
                user=request.user,
                product=option.variation,
                option=option
            )
            delete_item.delete()
        except Cart.DoesNotExist:
            logger.warning("No have cart item with product option id '%s'" % str(option_id))
    cart_items = get_cart_items(request)
    context = base_context_genre(request) 
    context.update({
        'cart_items': cart_items,
        'total': round(sum(map(itemgetter('totalPrice'), cart_items)), 2),
        'xhr_url': reverse('cart_count')
    })
    return render(request, "account/cart.html", context=context)


def LogInView(request):
    form = LogInForm(request.POST or None)
    context = base_context_genre(request)
    context.update( {'form': form })
    if request.method == "POST":
        next_page_url = request.GET.get('next')
        if form.is_valid():
            client_data = form.cleaned_data
            user = authenticate(username=client_data['login'],
            password=client_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next_page_url or '/')
        return render(request, 'account/login.html', context=context)
    return render(request, 'account/login.html', context=context)


@login_required(login_url="/account/login")
def LogOutView(request):
    logout(request)
    return HttpResponseRedirect("/")


def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            client_data = form.cleaned_data
            user = User.objects.create_user(
                username=client_data['login'],
                password=client_data['password']
            )
            user.email = client_data['email']
            user.save()
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'account/registration.html', context={
            'user': request.user,
            'form': form})
    form = RegisterForm()
    return render(request, 'account/registration.html', context={
        'user': request.user,
        'form': form})


@login_required(login_url="/account/login") 
def CartCountView(request):
    if request.method == 'GET':
        print(request.GET)
        product_id = int(request.GET.get('product_id'))
        cart_count = int(request.GET.get('cart_count'))
        option_id = int(request.GET.get('option_id'))
        cart = get_object_or_404(
            Cart,
            product_id=product_id,
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


@login_required(login_url="/account/login")
def orderView(request):
    form = OrderForm()
    context = base_context_genre(request)
    if request.method == "POST":
        print(request.POST)
        product_id_list = request.POST.getlist('product_id')
        option_id_list = request.POST.getlist('option_id')
        count_list = request.POST.getlist('count')
        product_list = Variation.objects.filter(id__in=map(lambda x: int(x), product_id_list))
        context.update(products_json(product_list, count_list))
        context.update( {'order_products': zip(
            product_id_list,
            option_id_list,
            count_list
        )})
        if 'create' in request.POST:
            form = OrderForm(request.POST)
            order_id = create_order(request, form)
            if order_id:
                return HttpResponseRedirect(reverse('thanks')+f"?order={order_id}")
            context.update( {'message': {'text': 'Не удалось создать заказ! :(', 'type': 'error'}})
    context.update( {'form': form })
    return render(request, 'account/order.html', context=context)


@login_required(login_url="/account/login")
def thanksView(request):
    context=base_context_genre(request)
    order = request.GET.get('order')
    if not order:
        return HttpResponseRedirect('/')
    context.update({'order': order})
    return render(request, 'account/thanks.html', context=context)