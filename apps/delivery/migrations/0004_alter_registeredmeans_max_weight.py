# Generated by Django 3.2.9 on 2022-03-14 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_alter_registeredmeans_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredmeans',
            name='max_weight',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
