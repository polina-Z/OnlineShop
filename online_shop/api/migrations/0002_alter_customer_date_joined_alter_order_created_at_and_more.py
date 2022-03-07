# Generated by Django 4.0 on 2022-01-29 15:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2022, 1, 29, 15, 33, 55, 706053, tzinfo=utc), verbose_name='Date Joined'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2022, 1, 29, 15, 33, 55, 709618, tzinfo=utc), verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2022, 1, 29, 15, 33, 55, 708307, tzinfo=utc), verbose_name='Created Date'),
        ),
    ]
