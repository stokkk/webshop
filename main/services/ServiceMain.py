from main.models import *
from django.shortcuts import get_object_or_404

from operator import attrgetter
from collections import defaultdict
from pprint import pprint

def product_detail_context(request, pk):
    """
    Return context.

    Context Template:
    {'productDetail':
        {
            'id': ...,
            'sku': ...,
            'name': ...,
            'brand': ...,
            'category': ...,
            'description': ...,
            'price': ...,
            'sale': ...,
            'photoList': [...],
        },
        'simpleAttributes': [
            {
                'name': ...,
                'values': [...]
            },
            ...
        ],
        'variableAttributes': [
            {
                'name': ...,
                'values': [...],
                'url': ...
            },
            ...
        ],
    }
    """
    context = {}
    product = get_object_or_404(ProductVar, pk=pk)

    photoList = [prodPhoto.photo for prodPhoto in product.productphoto_set.all()]
    value_set = product.product.values_set.all()
    grouped_values = defaultdict( list )
    for value in value_set:
        grouped_values[value.attribute].append(value)
    simpleAttributes = [{'name': key.title, 'values': list(                 # Простые аттрибуты.
        map(attrgetter('value'), value))
    } for key, value in grouped_values.items()]
    
    group_products = defaultdict( list )
    for varProd in ProductVar.objects.filter(group_id=product.group_id):    # словарь содержащий вариации товаров (модель - ProductVar)
        group_products[varProd.value.attribute].append(varProd)                   # сгруппированных по аттрибутам. {attribute: [ variation1, ... ]}
    variableAttributes = [ {'name': attr.title,                             # Вариативные аттрибуты.
    'values': [{'value': var.value.value, 'id': var.id} for var in prodVars],
    } for attr, prodVars in group_products.items()
    ]

    context = {'productDetail':
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
            'photoList': photoList,
        },
        'simpleAttributes': simpleAttributes,
        'variableAttributes': variableAttributes
    }
    return context
