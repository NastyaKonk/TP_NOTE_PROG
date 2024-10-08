# Generated by Django 5.1 on 2024-10-08 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monapp', '0002_productattribute_rename_prix_ht_product_price_ht_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mail', models.CharField(max_length=150)),
                ('adresse', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Fournisseur',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='Stock'),
        ),
        migrations.CreateModel(
            name='PrixProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fournisseur_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monapp.fournisseur', verbose_name='Fournisseur')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monapp.product', verbose_name='Produit')),
            ],
        ),
    ]
