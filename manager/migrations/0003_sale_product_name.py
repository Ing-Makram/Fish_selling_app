# Generated by Django 5.2 on 2025-06-11 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_command_product_command_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='product_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
