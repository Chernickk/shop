from basketapp.models import Basket


def basket(request):
    basket_ = []
    if request.user.is_authenticated:
        basket_ = Basket.objects.get(user=request.user)

    return {
        'basket': basket_
    }
