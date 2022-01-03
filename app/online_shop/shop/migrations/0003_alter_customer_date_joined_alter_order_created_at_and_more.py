# Generated by Django 4.0 on 2021-12-26 18:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_customer_date_joined_alter_customer_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 12, 26, 18, 25, 10, 26276, tzinfo=utc), verbose_name='Date Joined'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2021, 12, 26, 18, 25, 10, 29504, tzinfo=utc), verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2021, 12, 26, 18, 25, 10, 28178, tzinfo=utc), verbose_name='Created Date'),
        ),
    ]
