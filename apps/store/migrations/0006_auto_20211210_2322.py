# Generated by Django 3.2.9 on 2021-12-10 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_shop_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='active',
        ),
        migrations.AddField(
            model_name='shop',
            name='subscription_end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='logo',
            field=models.ImageField(null=True, upload_to='store_profiles/'),
        ),
    ]