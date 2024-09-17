from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse
import helpers
import helpers.billing

User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True

SUBSCRIPTION_PERMISSION = [
            ('advanced', 'Advanced Perm'), # subscriptions.advanced
            ('pro', 'Pro Perm'), #subscriptions.pro
            ('basic', 'Basic Perm'), #subscriptions.basic
            ('basic_ai', 'Basic AI Perm'),
        ]

class Subscriptions(models.Model):
    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(Permission,
    limit_choices_to={'content_type__app_label': 
    'subscriptions', 'codename__in':[x[0] for x in SUBSCRIPTION_PERMISSION]})
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    order =  models.IntegerField(default=-1, help_text='Ordering for Django pricing page')
    featured = models.BooleanField(default=True, help_text='Featured for Django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(help_text='Features for pricing separated by new line', blank=True, null=True)
    class Meta:
        permissions = SUBSCRIPTION_PERMISSION
        ordering = ['order', 'featured', '-updated']

    def __str__(self) -> str:
        return self.name


    def get_features_as_list(self):
        if not self.features:
            return []
        return [x.strip() for x in self.features.split('\n')]
    
    def save(self, *args, **kwargs):
        if not self.stripe_id:
            stripe_id = helpers.billing.create_product(
                name=self.name,
                metadata={
                    'subscription_plan_id': self.id
                },
                raw=False,
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)


class SubscriptionPrice(models.Model):
    class IntervalChoises(models.TextChoices):
        MONTHLY = 'month', 'Monthly'
        YEARLY = 'year', 'Yearly'

    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    interval = models.CharField(max_length=120, default=IntervalChoises.MONTHLY, choices=IntervalChoises.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    order = models.IntegerField(default=-1, help_text='Ordering on Django pricing page')
    featured = models.BooleanField(default=True, help_text='Featured on Django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['subscription__order', 'order', 'featured', '-price']

    def get_checkout_urls(self):
        return reverse("checkouts:sub_price_checkout", kwargs={'price_id':self.id})

    @property
    def stripe_currency(self):
        return "usd"
    
    @property
    def stripe_price(self):
        #remove decimal places
        return int(self.price * 100)
    
    @property
    def display_sub_name(self):
        if not self.subscription:
            return 'Plan'
        return self.subscription.name
    
    @property
    def display_feature_list(self):
        if not self.subscription:
            return []
        return self.subscription.get_features_as_list()

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id
    
    def save(self, *args, **kwargs):
        if not self.stripe_id and self.product_stripe_id is not None:
            stripe_id = helpers.billing.create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                interval=self.interval,
                product=self.product_stripe_id,
                metadata={
                    'subscription_plan_price_id': self.id
                },
                raw=False
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)
        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription=self.subscription,
                interval=self.interval
            ).exclude(id=self.id)
            qs.update(featured=False)

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.user.username} -  {self.subscription.name}'



def user_sub_post_save(sender, instance, *args, **kwargs):
    user_obj_instance = instance
    user = user_obj_instance.user
    subscription_obj = user_obj_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups)
    else:
        subs_qs = Subscriptions.objects.filter(active=True)
        if subscription_obj.id is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list('groups__id', flat=True)
        subs_groups_set = set(subs_groups)
        current_groups = user.groups.all().values_list('id', flat=True)
        groups_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - subs_groups_set
        final_ids = list(groups_ids_set | current_groups_set)
        user.groups.set(final_ids)

post_save.connect(user_sub_post_save, sender=UserSubscription)