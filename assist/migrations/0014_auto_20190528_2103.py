# Generated by Django 2.1.5 on 2019-05-28 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assist', '0013_auto_20190528_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistancereview',
            name='star_rating',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='assistancereview',
            name='text_rating',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
