# Generated by Django 5.0 on 2023-12-17 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_bid_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='user',
        ),
    ]
