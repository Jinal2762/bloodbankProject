# Generated by Django 3.2.7 on 2022-03-01 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbank_admin', '0010_auto_20220227_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='blood_grp',
            name='bloodgrp_status',
            field=models.CharField(default='0', max_length=120),
        ),
        migrations.AddField(
            model_name='bloodbank',
            name='description',
            field=models.CharField(default='desc', max_length=100),
        ),
        migrations.AddField(
            model_name='feedback',
            name='ratings',
            field=models.IntegerField(default=5),
        ),
    ]
