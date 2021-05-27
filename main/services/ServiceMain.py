from main.models import *
from django.shortcuts import get_object_or_404, reverse

from operator import attrgetter
from collections import defaultdict
from pprint import pprint


def product_detail_context(request, pk):
    product = get_object_or_404(Variation, pk=pk)
    return {'product':
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
            'photoList': list(map(attrgetter('photo'), product.productphoto_set.all())),
            'color': product.color
        },
        'option': get_options(product),
        'variations': get_variations(product)
    }


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