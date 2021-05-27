from django.shortcuts import reverse

def next_url_after_login(redirect_to: str, *args) -> str:
    return '%s?next=%s' % (
                reverse('login'),
                reverse(redirect_to, args=args)
            )

def calcTotalPrice(*args):
    price, sale, count = args
    result = 0.0
    if sale:
        result = price * (1 - sale / 100) * count
    else:
        result =  price * count 
    return round(result, 2)