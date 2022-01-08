# Generated by Django 3.2.9 on 2022-01-08 15:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='deliverymeans',
            unique_together={('owner', 'means')},
        ),
        migrations.AlterUniqueTogether(
            name='destination',
            unique_together={('means', 'location_from', 'location_to')},
        ),
    ]
