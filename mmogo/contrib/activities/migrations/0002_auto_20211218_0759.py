# Generated by Django 3.2.6 on 2021-12-18 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name': 'Activity', 'verbose_name_plural': 'Activities'},
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='event',
            new_name='action',
        ),
    ]