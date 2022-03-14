# Generated by Django 3.2.6 on 2021-08-24 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('from_address', models.CharField(max_length=255)),
                ('recipient', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('service', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('send_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('response', models.JSONField(blank=True, null=True)),
                ('service_email_id', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Emails',
                'verbose_name_plural': 'Emails',
                'db_table': 'emails',
            },
        ),
    ]
