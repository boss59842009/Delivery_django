# Generated by Django 5.0.6 on 2024-06-04 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0002_alter_deliveryaddress_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='distance',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]