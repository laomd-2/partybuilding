# Generated by Django 2.1.7 on 2019-05-15 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0002_auto_20190515_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='takepartin',
            name='last_modified',
        ),
        migrations.RemoveField(
            model_name='takepartin2',
            name='last_modified',
        ),
    ]