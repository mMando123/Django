# Generated by Django 5.1.4 on 2024-12-14 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_average_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='منتج مميز'),
        ),
    ]
