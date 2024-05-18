# Generated by Django 5.0.6 on 2024-05-11 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveryaddress',
            old_name='name',
            new_name='client',
        ),
        migrations.AlterField(
            model_name='client',
            name='orders',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='delivery_app.orderinfo'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='orders',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='delivery_app.orderinfo'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='orders',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='delivery_app.orderinfo'),
        ),
    ]