# Generated by Django 5.0.6 on 2024-05-11 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
