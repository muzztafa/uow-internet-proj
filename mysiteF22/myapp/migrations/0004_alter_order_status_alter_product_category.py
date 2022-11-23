# Generated by Django 4.1.2 on 2022-10-05 14:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_client_company_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 5, 14, 2, 34, 16656)),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='myapp.category'),
        ),
    ]