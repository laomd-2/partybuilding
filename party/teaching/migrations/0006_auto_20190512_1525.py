# Generated by Django 2.1.7 on 2019-05-12 15:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('teaching', '0005_auto_20190512_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='checkin_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='签到码'),
        )
    ]
