# Generated by Django 3.2.9 on 2022-03-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='means',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='means',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='transport_means/'),
        ),
    ]