# Generated by Django 4.2.16 on 2024-11-01 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_brand_oiltype_carforsale_carforrent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carforsale',
            old_name='decription',
            new_name='description',
        ),
    ]
