# Generated by Django 5.0.9 on 2024-09-17 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_init_email_customer_init_email_cofirmed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='init_email_cofirmed',
            new_name='init_email_confirmed',
        ),
    ]
