# Generated by Django 3.2.7 on 2022-01-31 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbank_admin', '0004_auto_20220130_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.BigIntegerField(),
        ),
    ]