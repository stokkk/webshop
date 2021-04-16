from django import template


register = template.Library()

def calcprice(price, sale_value):
    assert sale_value >= 0 and sale_value <= 100, "Sale value most be less than 100 and greater than zero."
    return round(price * (1 - sale_value / 100), 2)


register.filter('calcprice', calcprice)