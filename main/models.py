import random
import string
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.ForeignKey(
        'Photo',
        blank=True, null=True,
        default=None,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f"{self.name}"

class Brand(models.Model):
    name = models.CharField('Brand name', max_length=100, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    photo = models.ForeignKey(
        'Photo',
        blank=True, null=True,
        default=None,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f"{self.name}"

    
class Categories(models.Model):
    name = models.CharField('Имя категории', max_length=100, unique=True, default=None)
    slug = models.SlugField(max_length=50, unique=True, default=None)
    parent = models.ForeignKey(
        'self',
        default=None,
        blank=True,
        verbose_name='Категория родитель',
        null=True,
        on_delete=models.CASCADE
    )
    photo = models.ForeignKey(
        'Photo',
        blank=True, null=True,
        default=None,
        verbose_name='Фотография',
        on_delete=models.CASCADE
    )
    def __str__(self):
        return "{0}".format(self.name)


class Photo(models.Model):
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=100, default="", blank=True, null=True)
    def __str__(self):
        return f"img={self.id}"


class ProductPhoto(models.Model):
    product = models.ForeignKey('Variation', on_delete=models.CASCADE, default=None)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "id={0}, title={1}".format(self.product.id, self.photo.title)


class Product(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    )
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    pub_date = models.DateTimeField() # дата публикации
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.name)
        

class Options(models.Model):
    SIZE_CHOICES = (
        (str(i), str(i))
        for i in range(38, 47)
    )
    id = models.BigAutoField(primary_key=True)
    variation = models.ForeignKey('Variation', on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    count = models.IntegerField(default=0) # количество товаров

    def __str__(self):
        return f"{self.id} {self.variation.product.name}"

class Colors(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)
    image = models.ForeignKey('Photo', null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.name}"

class Variation(models.Model):

    VARTYPE_CHOICES = (
        ('simple', 'Simple'),
        ('variable', 'Variable'),
        ('variation', 'Variation'),
        ('option', 'Option')
    )
    id = models.BigAutoField(primary_key=True)
    sku = models.CharField(max_length=12, unique=True, blank=True) # артикул
    short_description = models.CharField(max_length=200, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reg_price = models.FloatField(default=0.0) # базовая цена
    sale_size = models.IntegerField(default=None, blank=True, null=True) # размер скидки
    color = models.ForeignKey(Colors, on_delete=models.CASCADE)
    def __str__(self):
        return f"id={self.id} color={self.color.name}"

    def generate_sku(self):
        random_symbols = string.ascii_uppercase + string.digits
        while not self.sku:
            sku = "{0}{1}{2}{3}-{4}{5}{6}{7}-{8}{9}".format(*(
                random.choice(random_symbols) for i in range(10)
            ))
            if not Variation.objects.filter(sku=sku):
                self.sku = sku
    
    def save(self, *args, **kwargs):
        self.generate_sku()
        super().save(*args, **kwargs)


    




        



