from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models.signals import post_save

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
    
    class Meta:
        permissions = SUBSCRIPTION_PERMISSION

    def __str__(self) -> str:
        return self.name
    

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