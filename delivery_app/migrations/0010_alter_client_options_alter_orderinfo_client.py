# Generated by Django 5.0.6 on 2024-05-13 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0009_alter_client_options_remove_client_orders_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['orderinfo__created_at']},
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='delivery_app.client'),
        ),
    ]
