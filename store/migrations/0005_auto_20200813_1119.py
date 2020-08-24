# Generated by Django 3.1 on 2020-08-13 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200813_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='product',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='customer',
        ),
        migrations.AddField(
            model_name='images',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='productos'),
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.images'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
