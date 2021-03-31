from django.contrib import admin

# Register your models here.
from .models import *

class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'brand_fk', 'pub_date', 'reg_price', 'sale_price', 'category_fk', 'sex', 'season')

admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPhoto)
admin.site.register(Categories)
admin.site.register(Attributes)
admin.site.register(AttributeAndCategory)
admin.site.register(ProductValue)
admin.site.register(Values)

