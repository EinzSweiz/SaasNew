from django.contrib import admin
from .models import Subscriptions, UserSubscription


class UserTabularInline(admin.TabularInline):
    model = UserSubscription
    extra = 1


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    fields = ['name', 'groups', 'active', 'permissions']
    inlines = [UserTabularInline, ]


admin.site.register(UserSubscription)