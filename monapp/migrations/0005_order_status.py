# Generated by Django 5.1 on 2024-10-15 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monapp', '0004_alter_prixproduct_options_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'In preparation'), (1, 'Passed'), (2, 'Received')], default=0),
        ),
    ]
