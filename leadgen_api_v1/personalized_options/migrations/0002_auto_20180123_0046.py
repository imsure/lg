# Generated by Django 2.0 on 2018-01-23 00:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalized_options', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='from_id',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(5)], verbose_name='ID of from location'),
        ),
    ]
