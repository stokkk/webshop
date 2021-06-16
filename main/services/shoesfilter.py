from django.db.models import Q
from main.models import Brand, Categories, Product, Colors, Variation
from collections import defaultdict

class ShoesFilter:

    def __init__(self, brand=None, price_from=None, price_to=None, # filters
                category=None, color=None, size=None, sale=None, search=None, sex=None):
        self._backend = defaultdict( lambda : None )
        if brand: self._backend['brand'] = (brand, self._brand_filter)
        if price_from: self._backend['price_from'] = (price_from, self._price_from_filter)
        if price_to: self._backend['price_to'] = (price_to, self._price_to_filter)
        if category: self._backend['category'] = (category, self._category_filter)
        if color: self._backend['color'] = (color, self._color_filter)
        if size: self._backend['size'] = (size, self._size_filter)
        if sale: self._backend['sale'] = (sale, self._sale_filter)
        if search: self._backend['search'] = (search, self._search_filter)
        if sex: self._backend['sex'] = (sex, self._sex_filter)
            
    def get_query(self, **kwargs):
        return Q(*(func(param) for param, func in self._backend.values()))
            
    def _brand_filter(self, brands):
        brand_list = Brand.objects.filter(slug__in=brands)
        product_list = Product.objects.filter(brand__in=brand_list)
        return Q(product__in=product_list)

    def _price_from_filter(self, price_from):
        return Q(reg_price__gte=price_from)

    def _price_to_filter(self, price_to):
        return Q(reg_price__lte=price_to)

    def _category_filter(self, categories):
        category_list = Categories.objects.filter(slug__in=categories)
        product_list = Product.objects.filter(category__in=category_list)
        return Q(product__in=product_list)

    def _color_filter(self, colors):
        colors_ = Colors.objects.filter(slug__in=colors)
        return Q(color__in=colors_)

    def _size_filter(self, sizes):
        return Q(options__size__in=sizes)

    def _sale_filter(self, sale):
        return Q(sale_size__gte=sale)
    
    def _search_filter(self, search):
        product_list = Product.objects.filter(name__icontains=search)
        return Q(product__in=product_list)

    def _sex_filter(self, sex):
        return Q(product__sex__in=sex)
