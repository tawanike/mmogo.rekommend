# Generated by Django 3.2.6 on 2021-12-25 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppinglists', '0006_auto_20211219_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppinglistcontributor',
            name='address',
        ),
        migrations.RemoveField(
            model_name='shoppinglistcontributor',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='shoppinglistcontributor',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='shoppinglistcontributor',
            name='role',
        ),
    ]
