from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from transliterate.utils import slugify
from operator import attrgetter
import random
import string
import datetime

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

    def get_countries(): 
        return [
            (country.id, country.name)
            for country in Country.objects.all()
        ]

        
    class Meta:
        verbose_name = "Страны"
        verbose_name_plural = "Страны"

class Brand(models.Model):
    name = models.CharField('Brand name', max_length=100, unique=True)
    slug = models.CharField('Slug', max_length=100, unique=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    photo = models.ForeignKey(
        'Photo',
        blank=True, null=True,
        default=None,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f"{self.name}"

    def get_brands(): 
        return {
            'brands': [
                {
                    'id': brand.id,
                    'name': brand.name,
                    'photo': Photo.get_photo(brand.photo),
                    'slug': brand.slug,
                    'country': brand.country.name,
                    'url': reverse('product_list') + f'/?brand={brand.name}'
                } 
                for brand in Brand.objects.all()
            ]
        }
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Брэнды"
        verbose_name_plural = "Брэнды"
    
class Categories(models.Model):
    name = models.CharField('Имя категории', max_length=100, unique=True, default=None)
    slug = models.CharField('Slug', max_length=100, unique=True, blank=True)
    photo = models.ForeignKey(
        'Photo',
        blank=True, null=True,
        default=None,
        verbose_name='Фотография',
        on_delete=models.CASCADE
    )
    def __str__(self):
        return "{0}".format(self.name)

    def get_categories():
        return {
            'categories': [
                {
                    'id': category.id,
                    'name': category.name,
                    'slug': category.slug,
                    'photo': Photo.get_photo(category.photo),
                    'url': reverse('product_list') + f'/?category={category.slug}'
                } 
                for category in Categories.objects.all()
            ]
        }
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"

class Photo(models.Model):
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=100, default="", blank=True, null=True)
    def __str__(self):
        return f"img={self.id}"

    def get_photo(photo : 'Photo'):
        if photo:
            return {
                'url': photo.photo.url,
                'title': photo.title
            }
        return photo
    class Meta:
        verbose_name = "Изображения"
        verbose_name_plural = "Изображения"

class ProductPhoto(models.Model):
    product = models.ForeignKey('Variation', on_delete=models.CASCADE, default=None)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "id={0}, title={1}".format(self.product.id, self.photo.title)
    class Meta:
        verbose_name = "Товары и Изображения"
        verbose_name_plural = "Товары и Изображения"

class Product(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    )
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.name)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)
    was_published_recently.short_description = "Дата публикации"
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'
    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"

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
    class Meta:
        verbose_name = "Опции"
        verbose_name_plural = "Опции"

class Colors(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)
    image = models.ForeignKey('Photo', null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.name}"
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Цвета"
        verbose_name_plural = "Цвета"

class Variation(models.Model):

    VARTYPE_CHOICES = (
        ('simple', 'Simple'),
        ('variable', 'Variable'),
        ('variation', 'Variation'),
        ('option', 'Option')
    )
    id = models.BigAutoField(primary_key=True)
    sku = models.CharField('Артикул', max_length=12, unique=True, blank=True) # артикул
    short_description = models.CharField('Описание',max_length=200, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reg_price = models.FloatField('Цена',default=0.0) # базовая цена
    sale_size = models.IntegerField('Скидка',default=None, blank=True, null=True) # размер скидки
    color = models.ForeignKey(Colors, verbose_name='Цвет', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации',default=timezone.now)
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
    class Meta:
        verbose_name = "Вариация"
        verbose_name_plural = "Вариации"

    def average_rate(self):
        comment_list = self.comments_set.all()
        if len(comment_list) == 0:
            return 0.0
        return sum(map(attrgetter('rate'), comment_list)) / len(comment_list)

    def save(self, *args, **kwargs):
        self.generate_sku()
        super().save(*args, **kwargs)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)
    was_published_recently.short_description = "Недавнее"
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'

class Comments(models.Model):
    product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=5)
    comment = models.TextField(max_length=1024)
    pub_date = models.DateTimeField()
    def __str__(self):
        return f"{self.user} {self.product} ({self.rate})"
        
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)
    was_published_recently.short_description = "Дата публикации"
    was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'pub_date'

    def get_comments(product_id):
        comments = Comments.objects.filter(product_id=product_id)
        return {
            'comments': [
                {
                    'user': comment.user.username,
                    'pub_date': comment.pub_date,
                    'rate': comment.rate,
                    'text': comment.comment
                }
                for comment in comments
            ]
        }
    class Meta:
        verbose_name = "Комментарии"
        verbose_name_plural = "Комментарии"

        



