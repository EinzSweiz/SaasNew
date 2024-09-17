from django.shortcuts import render
from .models import SubscriptionPrice

def subscription_price_view(request, interval='month'):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_mo = SubscriptionPrice.IntervalChoises.MONTHLY
    inv_yr = SubscriptionPrice.IntervalChoises.YEARLY
    if interval == 'year':
        object_list = qs.filter(interval=inv_yr)
    else:
        object_list = qs.filter(interval=inv_mo)
    return render(request, 'subscriptions/pricing.html', {
        'object_list': object_list,
        'interval': interval,
        })