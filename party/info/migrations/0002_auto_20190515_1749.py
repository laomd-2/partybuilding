# Generated by Django 2.1.7 on 2019-05-15 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='contacts',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='oldmember',
            name='contacts',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
