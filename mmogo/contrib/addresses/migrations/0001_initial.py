# Generated by Django 3.2.6 on 2021-10-29 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complex_name', models.CharField(blank=True, max_length=255, null=True)),
                ('street_address', models.CharField(max_length=255)),
                ('suburb', models.CharField(blank=True, max_length=255, null=True)),
                ('is_default', models.BooleanField(default=False)),
                ('city', models.CharField(max_length=255)),
                ('municipality', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('place_id', models.CharField(blank=True, max_length=255, null=True)),
                ('formatted_address', models.TextField(blank=True, max_length=255, null=True)),
                ('location', models.JSONField()),
                ('nearest_warehouse', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_address', to='locations.country')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'db_table': 'addresses',
            },
        ),
    ]