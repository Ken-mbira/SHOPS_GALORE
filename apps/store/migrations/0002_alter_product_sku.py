# Generated by Django 3.2.9 on 2022-01-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
