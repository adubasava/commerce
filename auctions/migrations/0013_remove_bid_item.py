# Generated by Django 5.0 on 2023-12-17 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_bid_starting_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='item',
        ),
    ]
