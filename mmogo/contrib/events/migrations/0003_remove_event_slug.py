# Generated by Django 3.2.6 on 2021-12-29 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20211229_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='slug',
        ),
    ]