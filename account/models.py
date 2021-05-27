from django.db import models
from django.contrib.auth.models import User
from main.models import Variation, Options


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    count = models.IntegerField(default=1)
    comment = models.CharField(max_length=500)
    commit = models.BooleanField(default=False)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    def __str__(self):
        return "{0}, {1}".format(self.user, self.product)

    class Meta:
        unique_together = (('user', 'product', 'option'),)

    
