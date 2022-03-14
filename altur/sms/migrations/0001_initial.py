# Generated by Django 3.2.6 on 2021-10-29 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_number', models.CharField(max_length=255)),
                ('recipient', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('service', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('send_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('response', models.JSONField(blank=True, null=True)),
                ('service_sms_id', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'SMS',
                'verbose_name_plural': 'SMSes',
                'db_table': 'sms',
            },
        ),
    ]