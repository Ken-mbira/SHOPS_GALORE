# Generated by Django 3.2.9 on 2021-12-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_shop_functional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]