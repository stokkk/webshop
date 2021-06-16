from main.utils import calcTotalPrice
from operator import attrgetter
from main.models import ProductPhoto, Options, Variation
from account.models import Cart, UserInfo, Addresses, OrderProducts, Order
from django.utils import timezone
from django.contrib.auth.models import User
def products_json(product_list, count_list):
    return {
        'products': [
            {
                'name': product.product.name,
                'id': product.id,
                'price': calcTotalPrice(product.reg_price, product.sale_size, 1),
                'count': number
            }
            for product, number in zip(product_list,count_list)
        ],
        'totalPrice': round(sum(
            map(
                lambda inst: calcTotalPrice(*inst),
                zip(
                    map(attrgetter('reg_price'), product_list),
                    map(attrgetter('sale_size'), product_list),
                    map(lambda item: int(item), count_list)
                )
            )
        ), 2),
    }



def create_order(request, form):
    product_id_list = map(lambda i: int(i), request.POST.getlist('product_id'))
    option_id_list = map(lambda i: int(i), request.POST.getlist('option_id'))
    count_list = map(lambda i: int(i), request.POST.getlist('count'))
    if any(map(
        lambda inst: inst[0].count < inst[1],
        zip(Options.objects.filter(id__in=option_id_list), count_list)
    )):
        return None
    if form.is_valid():
        cd = form.cleaned_data
        last_name = cd.get('last_name')
        first_name = cd.get('first_name')
        city = cd.get('city')
        street = cd.get('street')
        country = cd.get('country') # country_id
        postcode = cd.get('postcode')
        email = cd.get('email')
        phone = cd.get('phone')
        comment = cd.get('comment')
        delivery_type = cd.get('delivery_type')
        if 'save-data' in request.POST:
            try:
                user = User.objects.get(id=request.user.pk)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                try:
                    user_info = UserInfo.objects.get(user=user)
                    user_info.phone = phone,
                    user_info.address = Addresses.objects.update_or_create(
                            city=city,
                            street=street,
                            country_id=country,
                            zip_code=postcode
                        )
                    user_info.save()
                except UserInfo.DoesNotExist:
                    user_info = UserInfo.objects.create(
                        user=user,
                        phone=phone,
                        address=Addresses.objects.update_or_create(
                            city=city,
                            street=street,
                            country_id=country,
                            zip_code=postcode
                        )
                    )
                order = Order.objects.create(
                    user=user,
                    order_date=timezone.now(),
                    comment=comment,
                    delivery_type=delivery_type
                )

                for option, count in zip(
                    Options.objects.filter(id__in=option_id_list),
                    count_id_list
                ):
                    option.count -= count
                    option.save()
                    OrderProducts.objects.create(
                        product=option,
                        count=count,
                        order=order
                    )
                return order.id
                
            except User.DoesNotExist:
                print("User with pk = '%s' Does not exists" % request.user.pk)
                return None    
    return 19231293

    


def get_cart_items(request):
    return [
        {
            'product': {
                'id': item.product.id,
                'sku': item.product.sku,
                'name': item.product.product.name,
                'brand': item.product.product.brand.name,
                'price': item.product.reg_price,
                'sale': item.product.sale_size,
                'count': item.option.count,
                'size': {'id': item.option.id, 'value':item.option.size},
                'color': item.product.color.name,
                'photo': ProductPhoto.objects.filter(product=item.product).first().photo.photo
            },
            'number': item.count,
            'totalPrice': calcTotalPrice(
                item.product.reg_price,
                item.product.sale_size,
                item.count
            )
        } for item in Cart.objects.filter(user=request.user)
    ]
