# Generated by Django 3.2.7 on 2022-01-30 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbank_admin', '0003_auto_20220130_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateTimeField(),
        ),
    ]
