from django.db import models
from django.contrib.auth.models import User
from main.models import ProductVar


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVar, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    count = models.IntegerField(default=1)
    comment = models.CharField(max_length=500)
    commit = models.BooleanField(default=False)