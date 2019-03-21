# Generated by Django 2.1.7 on 2019-03-13 18:58

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0002_auto_20190223_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conference',
            name='key_dates',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]