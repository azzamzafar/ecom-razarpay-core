# Generated by Django 4.0 on 2023-01-31 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(max_length=500, verbose_name='description')),
                ('available', models.BooleanField()),
                ('quantity', models.PositiveSmallIntegerField()),
                ('photo', models.ImageField(upload_to='products')),
                ('amount', models.PositiveIntegerField()),
                ('category', models.ManyToManyField(related_name='products', to='store.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default=0)),
                ('order_amount', models.PositiveIntegerField(default=0)),
                ('currency', models.CharField(max_length=4)),
                ('Qty', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.PositiveIntegerField(default=0)),
                ('total_Qty', models.PositiveSmallIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=15, null=True)),
                ('shipping_address', models.TextField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoice', to='customers_auth.customer')),
                ('orders', models.ManyToManyField(related_name='orders_invoice', to='store.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.PositiveIntegerField(default=0)),
                ('total_Qty', models.PositiveSmallIntegerField(default=0)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='customers_auth.customer')),
                ('items', models.ManyToManyField(related_name='items_cart', to='store.Item')),
            ],
        ),
    ]
