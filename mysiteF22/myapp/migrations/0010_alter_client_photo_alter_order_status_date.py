# Generated by Django 4.1.1 on 2022-11-27 23:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_client_photo_alter_order_status_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='photo',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 27, 18, 33, 18, 641706)),
        ),
    ]
