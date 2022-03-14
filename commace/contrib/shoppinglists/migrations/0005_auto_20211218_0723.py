# Generated by Django 3.2.6 on 2021-12-18 05:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shoppinglists', '0004_auto_20211207_1531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'ordering': ['ordering', 'title'], 'verbose_name': 'Registry', 'verbose_name_plural': 'Registries'},
        ),
        migrations.AlterModelOptions(
            name='shoppinglistcontributor',
            options={'ordering': ['shoppinglist'], 'verbose_name': 'Registry Contributor', 'verbose_name_plural': 'Registry Contributors'},
        ),
        migrations.AlterModelOptions(
            name='shoppinglistitem',
            options={'ordering': ['shoppinglist'], 'verbose_name': 'Registry Item', 'verbose_name_plural': 'Registry Items'},
        ),
        migrations.RemoveField(
            model_name='shoppinglist',
            name='category',
        ),
        migrations.RemoveField(
            model_name='shoppinglist',
            name='user',
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='user',
            field=models.ManyToManyField(related_name='listcontributor', through='shoppinglists.ShoppingListContributor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shoppinglistcontributor',
            name='role',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]