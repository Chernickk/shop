from basketapp.models import Basket


def basket(request):
    basket_ = []
    if request.user.is_authenticated:
        basket_ = Basket.objects.filter(user=request.user)

    total = sum(bask.total for bask in basket_)

    return {
        'basket': basket_,
        'total': total,
    }
