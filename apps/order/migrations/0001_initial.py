# Generated by Django 3.2.9 on 2021-12-16 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('delivery', '0005_alter_destination_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('complete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('made_on', models.DateTimeField(auto_now_add=True)),
                ('staff_checked', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('id_password', models.CharField(max_length=256)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='KE')),
                ('token', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('delivery_means', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='delivery.deliverymeans')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='delivery.location')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShopDailyOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('pickup_means', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='daily_orders', to='delivery.deliverymeans')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='daily_orders', to='store.shop')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('seller_checked', models.BooleanField(default=False)),
                ('rider_checked', models.BooleanField(default=False)),
                ('staff_one_checked', models.BooleanField(default=False)),
                ('staff_two_checked', models.BooleanField(null=True)),
                ('daily_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item', to='order.shopdailyorders')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='order.cart')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='store.product')),
            ],
            options={
                'unique_together': {('product', 'cart')},
            },
        ),
    ]
