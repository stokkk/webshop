from django.db import models

# Create your models here.
import random
import string

class Brand(models.Model):
    name = models.CharField('Brand name', max_length=100, unique=True)
    def __str__(self):
        return "{0}".format(self.name)

    
class Categories(models.Model):
    name = models.CharField('Имя категории', max_length=100, unique=True, default=None)
    slug = models.SlugField(max_length=50, unique=True, default=None)
    parent = models.ForeignKey('self', default=None, blank=True, verbose_name='Категория родитель', null=True, on_delete=models.CASCADE)
    def __str__(self):
        return "{0}".format(self.name)


class Attributes(models.Model):
    TYPE_CHOICES = (
        ('simple', 'Simple'),
        ('variable', 'Variable'),
        ('variation', 'Variation')
    )
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    attribute_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    def __str__(self):
        return "{0} ({1})".format(self.title, self.attribute_type)


class AttributeAndCategory(models.Model):
    category= models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attributes, verbose_name='Аттрибут', on_delete=models.CASCADE)
    def __str__(self):
        return "category.name={0}, attribute.slug={1}>".format(self.category.name, self.attribute.slug)


class Values(models.Model):
    value = models.CharField(max_length=200)
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True, default=None)
    def __str__(self):
        return "{1}: {0}".format(self.value, self.attribute.title)
    
    def save(self, *args, **kwargs):
        if (self.attribute.attribute_type != "simple"
        ) and (self.product is not None):
            raise AttributeError("Attribute of value have type '{0}'. Most be a simple".format(self.attribute.attribute_type))
        super().save(*args,**kwargs)


class Photo(models.Model):
    photoUrl = models.CharField(max_length=255, blank=True, null=True)
    photoBin = models.ImageField(upload_to='images/', blank=True, null=True)
    photoName = models.CharField(max_length=100, default="No Image")
    def __str__(self):
        return "img={0}".format(self.photoName)


class ProductPhoto(models.Model):
    product = models.ForeignKey('ProductVar', on_delete=models.CASCADE, default=None)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "sku={0}, name={1}".format(self.product.sku,self.photo.photoName)


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
    season = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.name)
        

class ProductVar(models.Model):
    id = models.BigAutoField(primary_key=True)
    sku = models.CharField(max_length=12, unique=True, blank=True) # артикул
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.ForeignKey(Values, on_delete=models.CASCADE)
    reg_price = models.FloatField(default=0.0)
    sale_size = models.IntegerField(default=None, blank=True, null=True)
    count = models.IntegerField(default=0) # количество товаров с таким значением атрибута
    group_id = models.PositiveIntegerField(default=None, blank=True, null=True)
    def __str__(self):
        return "id={0}, value={1}".format(self.id, self.value.value)
    
    def save(self, *args, **kwargs):
        random_symbols = string.ascii_uppercase + string.digits
        while not self.sku:
            sku = (random.choice(random_symbols) for i in range(10))
            sku = "{0}{1}{2}{3}-{4}{5}{6}{7}-{8}{9}".format(*sku)
            if not ProductVar.objects.filter(sku=sku):
                self.sku = sku
        super().save(*args,**kwargs)


        



