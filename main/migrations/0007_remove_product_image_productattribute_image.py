# Generated by Django 4.1.4 on 2023-01-07 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_banner_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='image',
            field=models.ImageField(null=True, upload_to='product_imgs/'),
        ),
    ]
