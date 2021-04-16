from django.contrib import admin

# Register your models here.
from .models import *


class ProductPhotoInline(admin.StackedInline):
    model = ProductPhoto
    extra = 1


class ProductVarInline(admin.StackedInline):
    model = ProductVar
    extra = 1


class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ('get_product_sku', 'get_photo_name')

    def get_product_sku(self, obj):
        return obj.product.sku
    get_product_sku.short_description = "SKU"

    def get_photo_name(self, obj):
        return obj.photo.photoName
    get_photo_name.short_description = "Имя фото"


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('get_photo_name',)
    inlines = (ProductPhotoInline,)

    def get_photo_name(self, obj):
        return obj.photoName
    get_photo_name.short_description = "Имя фото"
    def get_product_sku(self, obj):
        return obj.productphoto_set.filter(photo=obj.id)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'pub_date', 'category', 'sex', 'season')
    search_fields = ('name',)
    list_filter = ('name', 'brand', 'pub_date', 'category', 'sex', 'season')
    list_per_page = 25
    inlines = (ProductVarInline,)


class ProductVarAdmin(admin.ModelAdmin):
    list_display = (
        'sku', 'get_product_name', 'count', 'reg_price', 
        'group_id', 'get_attribute_name', 'get_value'
    )
    search_fields = ('sku',)
    list_filter = ('sku', 'count', 'reg_price')
    inlines = (ProductPhotoInline,)

    def get_value(self, obj):
        return obj.value.value
    get_value.short_description = 'Значение'

    def get_attribute_name(self, obj):
        return obj.value.attribute.title
    get_attribute_name.short_description = 'Аттрибут'

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Имя товара'



admin.site.register(Brand)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPhoto, ProductPhotoAdmin)
admin.site.register(Categories)
admin.site.register(Attributes)
admin.site.register(AttributeAndCategory)
admin.site.register(ProductVar, ProductVarAdmin)
admin.site.register(Values)

