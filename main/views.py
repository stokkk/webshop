from django.db.models import base
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from .services.contextmanage import base_context_genre, product_detail_context
from .services.shoesfilter import ShoesFilter
from .services.mainservice import add_to_cart, add_comment
from main.utils import calcTotalPrice, next_url_after_login, make_url
from shoestore.settings import PAGINATOR_PACK

from .models import *
from .forms import CommentForm

from operator import attrgetter

app_name = 'main'


def get_first_photo(product):
    photo = product.productphoto_set.first()
    if photo:
        return Photo.get_photo(photo.photo)
    return None


def index(request):
    products = Variation.objects.filter()[:6]
    top_category = Categories.objects.get(slug='krossovki')
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
        'topcategory': {
            'url': reverse('product_list')+f'?category={top_category.slug}',
            'title': '#кроссовки',
            'img': top_category.photo.photo.url
        }
    }
    context.update( base_context_genre(request) )
    context.update( Categories.get_categories() )
    return render(request, 'main/index.html', context)


def get_shoes_list(*args, **kwargs):
    orderby = kwargs['orderby'] if 'orderby' in kwargs else '-reg_price'
    return [
        {
            'id': variation.id,
            'name': variation.product.name,
            'brand': variation.product.brand.name,
            'photo': get_first_photo(variation),
            'price': variation.reg_price,
            'sale': variation.sale_size,
            'new_price': calcTotalPrice(variation.reg_price, variation.sale_size, 1),
            'new': variation.was_published_recently(),
            'not_in_stock': not any(map(lambda inst: inst.count > 0, variation.options_set.all())),
            'hot': variation.average_rate() >= 4.0
        }
        for variation in Variation.objects.filter(*args).order_by(orderby).distinct()
    ]


def get_sort_ordering(order_by):
    order_dict = {
        'date-new': ('-pub_date', 'сначала новые'),
        'date-old': ('pub_date', 'сначала старые'),
        'name-asc': ('product__name', 'названию, A-Z'),
        'name-desc': ('-product__name', 'названию, Z-A'),
        'price-asc': ('reg_price', 'цена, возростанию'),
        'price-desc': ('-reg_price', 'цена, убыванию')
    }
    sort_order = order_dict.get(order_by)
    if sort_order:
        return sort_order
    else:
        return order_dict['price-desc']

def shoes_list(request):
    sort_by = request.GET.get('sort')
    if not sort_by:
        return HttpResponseRedirect(make_url(request.build_absolute_uri(), params=(('sort', 'price-desc'),)))
    sort_order, current_sort = get_sort_ordering(sort_by)
    shoes_filter = ShoesFilter(
        brand=request.GET.getlist('brand'),
        price_from=request.GET.get('price-start'),
        price_to=request.GET.get('price-end'),
        category=request.GET.getlist('category'),
        color=request.GET.getlist('color'),
        size=request.GET.getlist('size'),
        sale=request.GET.get('sale'),
        search=request.GET.get('search'),
        sex=request.GET.getlist('sex')
    )
    query_set = shoes_filter.get_query()
    paginator = Paginator(get_shoes_list(query_set, orderby=sort_order), PAGINATOR_PACK)
    page = request.GET.get('page')
    product_list = paginator.get_page(page)

    context = dict()
    context.update( base_context_genre(request) )
    context.update( Categories.get_categories() )
    context.update({
        'product_list': product_list,
        'shoes_number': paginator.count,
        'colors': Colors.objects.all(),
        'current_sort': current_sort,
        'sizes': [ {'id': str(i) + 'SIZE', 'value': str(i)} for i in range(38, 47)],
        'max_price': str(Variation.objects.order_by('-reg_price').first().reg_price + 0.01).replace(',', '.'),
    })
    return render(request, 'main/shoes_list.html', context=context)


def product_detail(request, pk):
    context = product_detail_context(request, pk=pk)
    form = CommentForm()
    context.update( {'form': form} )
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                next_url_after_login('product_detail', pk)
            )
        if 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                context.update( add_comment(
                    request.user,
                    request.POST['comment'],
                    request.POST['rate'],
                    pk
                ))
        else:
            context.update( add_to_cart(
                request.user,
                request.POST['pk'],
                int(request.POST['number']),
                int(request.POST['option_id'])
            ) )
    
    return render(request, 'main/product_detail.html', context)
