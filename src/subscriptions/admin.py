from django.contrib import admin
from .models import Subscriptions, UserSubscription, SubscriptionPrice


class UserTabularInline(admin.TabularInline):
    model = UserSubscription
    extra = 1

class SubscriptionPriceInline(admin.TabularInline):
    readonly_fields = ['stripe_id']
    model = SubscriptionPrice
    can_delete = False
    extra = 0

@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    fields = ['name', 'groups', 'active', 'permissions', 'stripe_id', 'order', 'features']
    list_display = ['name', 'active', 'stripe_id']
    readonly_fields = ['stripe_id']
    inlines = [UserTabularInline, SubscriptionPriceInline]


admin.site.register(UserSubscription)