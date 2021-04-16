from main.models import Product

import random

format_sku = "{0}{1}{2}{3}-{4}{5}{6}{7}-{8}{9}"

def gen_sku():
    sku = ""
    try:
        while True:
            random_list = (random.randint(0,10) for _ in range(10))
            sku = format_sku.format(*random_list)
            p = Product.objects.get(sku=sku)
    except Product.DoesNotExist:
        return sku
