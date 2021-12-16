# Generated by Django 3.2.9 on 2021-12-16 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
        ('order', '0003_alter_order_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopdailyorders',
            name='storage_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_orders', to='storage.storage'),
        ),
    ]
