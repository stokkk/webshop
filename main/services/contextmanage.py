from main.utils import calcTotalPrice
from main.models import *
from django.shortcuts import get_object_or_404, reverse

from operator import attrgetter
from main.utils import calcTotalPrice

def product_detail_context(request, pk):
    product = get_object_or_404(Variation, pk=pk)
    context = {'product':
        {
            'id': product.id,
            'sku': product.sku,
            'name': product.product.name,
            'brand': product.product.brand.name,
            'category': product.product.category.name,
            'shortdescription': product.short_description,
            'description': product.product.description,
            'price': product.reg_price,
            'sale': product.sale_size,
            'new_price': calcTotalPrice(product.reg_price, product.sale_size, 1),
            'photoList': list(map(attrgetter('photo'), product.productphoto_set.all())),
            'color': product.color
        },
        'option': get_options(product),
        'variations': get_variations(product)
    }
    context.update( base_context_genre(request) )
    context.update( Comments.get_comments(pk) )
    context.update( {'number_of_comments': product.comments_set.count()})
    return context


def get_options(product):
    return {
        'name': 'Размер',
        'sizes': [
            { 
                'id': opt.id,
                'count': opt.count,
                'value': opt.size
            }
            for opt in product.options_set.all()
        ]
    }

def base_context_genre(request):
    context = {
        'user': request.user,
    }
    context.update( Brand.get_brands() )
    context.update( Categories.get_categories())
    return context
    
def get_variations(product):
    return [
        {
            'id': var.id,
            'url': reverse('product_detail', args=(var.id,)),
            'color': {
                'name': var.color.name,
                'slug': var.color.slug
            }
        }
        for var in product.product.variation_set.all()
    ]