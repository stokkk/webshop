from django.shortcuts import reverse
from urllib.parse import quote, parse_qsl,urlencode, urlparse, urlunparse
from collections import defaultdict

def next_url_after_login(redirect_to: str, *args) -> str:
    return '%s?next=%s' % (
                reverse('login'),
                reverse(redirect_to, args=args)
            )


def make_url(url, params=None):
    parse_url = urlparse(url)
    query_parse = parse_qsl(parse_url.query, keep_blank_values=True)
    if isinstance(params, str):
        query_parse += parse_qsl(urlparse(params).query, keep_blank_values=True)
    elif isinstance(params, tuple) or isinstance(params, list):
        query_parse += params
    else:
        raise AttributeError("Parameter 'params' most be a string or tuple or list.")
    return urlunparse((
        parse_url.scheme,
        parse_url.netloc,
        parse_url.path,
        parse_url.params,
        urlencode(query_parse, quote_via=quote),
        parse_url.fragment
    ))


def calcTotalPrice(*args):
    price, sale, count = args
    result = 0.0
    if sale:
        result = price * (1 - sale / 100) * count
    else:
        result =  price * count 
    return round(result, 2)