from django.contrib import admin

# Register your models here.
from .models import *


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1


class PhotoAdmin(admin.ModelAdmin):
    inlines = (ProductPhotoInline,)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'pub_date', 'reg_price', 'sale_price', 'category', 'sex', 'season')
    inlines = (ProductPhotoInline,)
    search_fields = ['name']


admin.site.register(Brand)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPhoto)
admin.site.register(Categories)
admin.site.register(Attributes)
admin.site.register(AttributeAndCategory)
admin.site.register(ProductValue)
admin.site.register(Values)

