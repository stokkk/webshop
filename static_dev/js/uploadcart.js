function sendAjax(cart, url) {
    $.get(
        url,
        {
            'option_id': cart.id,
            'cart_count': parseInt(cart.value),
            'product_id': cart.nextElementSibling.value
        },
        function (response) {
            var citem = cart.parentNode.parentNode.nextElementSibling;
            //console.log(response.totalItemPrice);
            //console.log(response.totalPrice);
            citem.getElementsByClassName("price")[0].textContent = response.totalItemPrice.toFixed(2);
            $.find('.cart-text p')[1].textContent = response.totalPrice.toFixed(2) + " BYN";
            cart.value = response.count;
        }
    )
}