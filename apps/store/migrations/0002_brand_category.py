# Generated by Django 3.2.9 on 2021-12-10 05:45

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='brand_logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_length=100', max_length=100, verbose_name='category name')),
                ('slug', models.SlugField(help_text='format:required, letters, numbers, underscore, hyphens', max_length=200, verbose_name='category safe URL')),
                ('is_active', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, help_text='Format: not required', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='store.category', verbose_name='parent of category')),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product categories',
            },
        ),
    ]