# Generated by Django 2.1.5 on 2019-02-11 13:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ('-date', 'name'), 'verbose_name': '会议/活动', 'verbose_name_plural': '会议/活动'},
        ),
        migrations.AlterField(
            model_name='activity',
            name='credit',
            field=models.FloatField(choices=[(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (5.5, 5.5), (6.0, 6.0), (6.5, 6.5), (7.0, 7.0), (7.5, 7.5), (8.0, 8.0), (8.5, 8.5), (9.0, 9.0), (9.5, 9.5), (10.0, 10.0), (10.5, 10.5), (11.0, 11.0), (11.5, 11.5), (12.0, 12.0), (12.5, 12.5), (13.0, 13.0), (13.5, 13.5), (14.0, 14.0), (14.5, 14.5), (15.0, 15.0), (15.5, 15.5), (16.0, 16.0), (16.5, 16.5), (17.0, 17.0), (17.5, 17.5), (18.0, 18.0), (18.5, 18.5), (19.0, 19.0), (19.5, 19.5), (20.0, 20.0)], verbose_name='学时数'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='时间'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=100, verbose_name='主题'),
        ),
    ]