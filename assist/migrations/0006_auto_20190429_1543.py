# Generated by Django 2.1.5 on 2019-04-29 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assist', '0005_userprofilemodel_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistancerequest',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assistancerequest',
            name='lodge_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
