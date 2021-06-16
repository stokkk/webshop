from django.db import models
from django.contrib.auth.models import User
from main.models import Variation, Options, Country


class Order(models.Model):
    DELIVERY_CHOICES = (
        ('mail', 'Почтой'),
        ('self', 'Самовызов'),
        ('home', 'Доставка на дом')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    close_date = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=500)
    commit = models.BooleanField(default=False)
    delivery_type = models.CharField(max_length=20, default="self", choices=DELIVERY_CHOICES)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderProducts(models.Model):
    product = models.ForeignKey(Options, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    def __str__(self):
        return "{0}, {1}".format(self.user, self.product)

    class Meta:
        unique_together = (('user', 'product', 'option'),)
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey('Addresses', on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.user}"

    
class Addresses(models.Model):
    street = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=25)
    def __str__(self):
        return f"{self.city} {self.street}"

