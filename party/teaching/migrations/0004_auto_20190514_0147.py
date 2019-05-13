# Generated by Django 2.1.7 on 2019-05-14 01:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import teaching.models


class Migration(migrations.Migration):
    dependencies = [
        ('teaching', '0003_auto_20190510_0124'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.IntegerField()),
                ('netid', models.IntegerField()),
                ('ip', models.CharField(max_length=50)),
            ],
        ),

        migrations.AddField(
            model_name='activity',
            name='checkin_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='签到码'),
        ),
        migrations.AddField(
            model_name='activity',
            name='checkin_qr',
            field=teaching.models.NullableImageField(blank=True, editable=False, null=True,
                                                     upload_to=teaching.models.upload_to, verbose_name='签到二维码'),
        ),

        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together={('activity_id', 'netid')},
        ),

    ]
