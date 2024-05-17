# Generated by Django 5.0.6 on 2024-05-17 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_total_price_ordereditem_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[(0, 'Cart'), (1, 'Order Confirmed'), (2, 'Order Processed'), (3, 'Order Delivered'), (4, 'Order Rejected'), (5, 'Order Completed')], default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Live'), (0, 'Delete')], default=1),
        ),
    ]