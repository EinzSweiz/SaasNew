# Generated by Django 5.0.9 on 2024-09-16 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='init_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='init_email_cofirmed',
            field=models.BooleanField(default=False),
        ),
    ]
