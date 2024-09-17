from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from subscriptions.models import SubscriptionPrice

def subscription_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session['checkout_subscription_price_id'] = price_id
    return redirect(reverse('checkouts:checkout_redirect'))


@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get('checkout_subscription_price_id')
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)
    except:
        obj = None
    if checkout_subscription_price_id is None or obj is None:
        return redirect('/pricing/month')
    customer_stripe_id = request.user.customer.stripe_id
    return redirect('/checkout/abc')


def checkout_finalize_view(request):
    return 