# Generated by Django 4.2 on 2025-06-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=9000, max_digits=10),
            preserve_default=False,
        ),
    ]
