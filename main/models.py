from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name.__str__()

    
class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True, default=None)
    slug = models.SlugField(max_length=50, unique=True, default=None)
    parent_id = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name.__str__()

class Attributes(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    attribute_type = models.CharField(max_length=50)
    def __str__(self):
        return self.slug.__str__()


class AttributeAndCategory(models.Model):
    category_fk = models.ForeignKey(Categories, on_delete=models.CASCADE)
    attribute_fk = models.ForeignKey(Attributes, on_delete=models.CASCADE)


class Values(models.Model):
    value = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    attribute_fk = models.ForeignKey(Attributes, on_delete=models.CASCADE)
    def __str__(self):
        return self.slug.__str__() 


class ProductPhoto(models.Model):
    photoUrl = models.CharField(max_length=255, blank=True, null=True)
    photoBin = models.ImageField(upload_to='images/', blank=True, null=True)
    photoName = models.CharField(max_length=100, default="No Image.")
    # product_fk = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.photoName.__str__()


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand_fk = models.ForeignKey(Brand, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    category_fk = models.ForeignKey(Categories, on_delete=models.CASCADE)
    reg_price = models.FloatField(default=0.0)
    sale_price = models.FloatField(default=0.0, blank=True, null=True)
    sex = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    photo_fk = models.ManyToManyField(ProductPhoto)
    def __str__(self):
        return self.name.__str__()
        
        
class ProductValue(models.Model):
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    value_fk = models.ForeignKey(Values, on_delete=models.CASCADE)

