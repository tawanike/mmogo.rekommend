# Generated by Django 3.2.6 on 2021-12-05 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_auto_20211203_0544'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Checkout Page'), (2, 'Address Page'), (3, 'Payment Pending'), (4, 'Paid')], default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('contacted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'db_table': 'cart',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('quantity', models.IntegerField(default=0)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Picked'), (2, 'Out of Stock'), (3, 'Alternative Picked')], default=0)),
                ('alt_product_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7, null=True)),
                ('alt_product_quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('alt_product_status', models.IntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Picked'), (2, 'Out of Stock'), (3, 'Alternative Picked')], null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('alt_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_item_alt_product', to='products.product')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cart')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'db_table': 'cart_item',
                'ordering': ['cart'],
            },
        ),
    ]