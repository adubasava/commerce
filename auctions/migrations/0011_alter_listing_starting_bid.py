# Generated by Django 5.0 on 2023-12-17 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_bid_item_bid_starting_bid_alter_listing_starting_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.FloatField(),
        ),
    ]
