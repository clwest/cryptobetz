# Generated by Django 4.1.7 on 2023-03-17 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrencys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nfts',
            name='unique_address',
            field=models.FloatField(blank=True, null=True),
        ),
    ]