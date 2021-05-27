from django.contrib import admin

# Register your models here.
from .models import *


class ProductPhotoInline(admin.StackedInline):
    model = ProductPhoto
    extra = 1


class ProductVarInline(admin.StackedInline):
    model = Variation
    extra = 1


class OptionInline(admin.StackedInline):
    model = Options
    extra = 1


class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ('get_product_sku', 'get_title')

    def get_product_sku(self, obj):
        return obj.product.sku
    get_product_sku.short_description = "SKU"

    def get_title(self, obj):
        return obj.photo.title
    get_title.short_description = "Описание"


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('get_title',)

    def get_title(self, obj):
        return obj.title
    get_title.short_description = "Описание"
    def get_product_sku(self, obj):
        return obj.productphoto_set.filter(photo=obj.id)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'pub_date', 'category', 'sex')
    search_fields = ('name',)
    list_filter = ('name', 'brand', 'pub_date', 'category', 'sex')
    list_per_page = 25
    inlines = (ProductVarInline,)


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_product_name', 'get_color', 'reg_price', 'sale_size'
    )
    # search_fields = ('sku',)
    # list_filter = ('sku', 'count', 'reg_price')
    inlines = (ProductPhotoInline, OptionInline)

    def get_color(self, inst):
        return inst.color.name
    get_color.short_description = "Цвет"

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Имя товара'


class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'size', 'count')


admin.site.register(Brand)
admin.site.register(Country)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPhoto, ProductPhotoAdmin)
admin.site.register(Categories)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Colors)
admin.site.register(Options, OptionAdmin)

