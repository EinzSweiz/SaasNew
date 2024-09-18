from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import helpers
import helpers.billing
from subscriptions.models import SubscriptionPrice, Subscriptions, UserSubscription
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest


User = get_user_model()

BASE_URL = settings.BASE_URL
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
    sucess_url_path = reverse('checkouts:checkout_success')
    pricing_url_path = reverse('subscriptions:pricing', kwargs={'interval': 'monthly'})
    sucess_url = f'{BASE_URL}{sucess_url_path}'
    cancel_url = f'{BASE_URL}{pricing_url_path}'
    customer_stripe_id = request.user.customer.stripe_id
    price_stripe_id = obj.stripe_id
    url = helpers.billing.start_checkout_session(
        customer_stripe_id,
        success_url=sucess_url,
        cancel_url=cancel_url,
        price_stripe_id=price_stripe_id,
        raw=False,

    )
    return redirect(url)


from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import get_user_model
from subscriptions.models import Subscriptions, UserSubscription

User = get_user_model()

def checkout_finalize_view(request):
    session_id = request.GET.get('session_id')
    
    # Retrieve customer_id and plan_id from session
    customer_id, plan_id = helpers.billing.get_checkout_customer_plan(session_id=session_id)

    # Get the subscription object
    try:
        subscription_obj = Subscriptions.objects.get(subscriptionprice__stripe_id=plan_id)
    except Subscriptions.DoesNotExist:
        return HttpResponseBadRequest('Subscription plan not found.')

    # Get the user object
    try:
        user_obj = User.objects.get(customer__stripe_id=customer_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest('User not found. Please contact support.')

    # Check if UserSubscription already exists
    try:
        _user_sub_obj = UserSubscription.objects.get(user=user_obj)
        _user_sub_obj.subscription = subscription_obj  # Update the subscription
        _user_sub_obj.save()
    except UserSubscription.DoesNotExist:
        # Create a new UserSubscription
        _user_sub_obj = UserSubscription.objects.create(
            user=user_obj, 
            subscription=subscription_obj
        )
    
    # If something goes wrong during the process
    if None in [_user_sub_obj, user_obj, subscription_obj]:
        return HttpResponseBadRequest('There was an error with your account, please contact us.')

    context = {
        'subscription': subscription_obj,
        'user': user_obj
    }

    return render(request, 'checkouts/success.html', context=context)
