# Generated by Django 4.1.7 on 2023-03-18 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrencys', '0005_alter_cryptocurrency_ath_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='ath_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='atl_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
