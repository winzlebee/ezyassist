# Generated by Django 2.1.5 on 2019-04-01 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assist', '0004_auto_20190324_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilemodel',
            name='registration',
            field=models.CharField(default='AA-AA-AA', max_length=20),
            preserve_default=False,
        ),
    ]
