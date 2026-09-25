def cart_counter(request):
    """
    Calcule le nombre total d'articles dans le panier.
    Le résultat devient disponible sur toutes les pages
    avec la variable {{ cart_count }}.
    """

    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    total = 0

    for item in cart.values():

        if isinstance(item, dict):
            quantity = item.get("quantity", 1)
        else:
            quantity = item

        try:
            total += int(quantity)
        except (TypeError, ValueError):
            total += 1

    return {
        "cart_count": total
    }