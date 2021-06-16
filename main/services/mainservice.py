from django.shortcuts import get_object_or_404
from django.utils import timezone
from main.models import Options, Comments
from account.models import Cart

def add_to_cart(user, product_id, number, option_id):
    message_success = "Товар успешно добвлен в корзину."
    message_failure = "На складе нету нужного количества товара."
    option = get_object_or_404(Options, pk=option_id)
    if option.count < number:
        return {'message': {'text': message_failure, 'type': 'failure'}}
    try:
        cart_item = Cart.objects.get(       # если будет более одного дубликата
            user=user,                      # выдаст MultiplyObjectsReturned
            product_id=product_id,
            option_id=option_id
        )
        if cart_item.count + number > option.count:
            return {'message': {'text': message_failure, 'type': 'failure'}}
        cart_item.count += number
        cart_item.save()
    except Cart.DoesNotExist:
        cart_item = Cart.objects.create(
            user=user,
            product_id=product_id,
            count=number,
            option_id=option_id
        )
    return {'message': {'text': message_success, 'type': 'success'}}


def add_comment(user, comment, rate, product_id):
    if Comments.objects.filter(user_id=user.pk, product_id=product_id).exists():
        return {'message': {'text': 'Вы можете оставить только один комментарий!', 'type': 'failure'}}
    comment_instace = Comments.objects.create(
        product_id=product_id,
        user_id=user.pk,
        rate=rate,
        comment=comment,
        pub_date=timezone.now()
    )
    if comment_instace:
        return {'message': {'text': 'Комментарий успешно добавлен.', 'type': 'success'}}
    return {'message': {'text': 'Произошла ошибка!', 'type': 'failure'}}