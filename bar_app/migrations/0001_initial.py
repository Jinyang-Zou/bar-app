# Generated by Django 5.0.4 on 2024-04-16 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Bar',
                'verbose_name_plural': 'Bars',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ref', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Reference',
                'verbose_name_plural': 'References',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar_app.bar')),
                ('items', models.ManyToManyField(to='bar_app.orderitem')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='orderitem',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar_app.reference'),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField(default=0)),
                ('bar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar_app.bar')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar_app.reference')),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
                'ordering': ['id'],
            },
        ),
    ]
