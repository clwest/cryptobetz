# Generated by Django 4.1.7 on 2023-03-17 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrencys', '0003_remove_nfts_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nfts',
            name='total_supply',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
