# Generated by Django 5.0.6 on 2024-05-13 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0011_alter_client_options_alter_orderinfo_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='status',
            field=models.CharField(choices=[('confirmed', 'Підтверджено'), ('on_the_way', 'В дорозі'), ('delivered', 'Доставлено'), ('canceled', 'Відмінено')], default='confirmed', max_length=20),
        ),
    ]
