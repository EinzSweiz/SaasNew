from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ['user', 'stripe_id', 'init_email', 'init_email_confirmed']