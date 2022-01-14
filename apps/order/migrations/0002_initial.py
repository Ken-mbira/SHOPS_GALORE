# Generated by Django 3.2.9 on 2022-01-08 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('delivery', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopdailyorders',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='daily_orders', to='store.shop'),
        ),
        migrations.AddField(
            model_name='shopdailyorders',
            name='storage_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_orders', to='storage.storagefacility'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='daily_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item', to='order.shopdailyorders'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='order.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='store.product'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='transit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='storage.dailytransit'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_means',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='delivery.deliverymeans'),
        ),
        migrations.AddField(
            model_name='order',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='delivery.location'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='order.cart'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='store.product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('product', 'cart')},
        ),
    ]