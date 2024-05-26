# Generated by Django 5.0.6 on 2024-05-24 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0016_alter_orderinfo_additional_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='driver', to='delivery_app.driver'),
        ),
    ]