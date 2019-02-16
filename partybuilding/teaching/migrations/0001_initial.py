# Generated by Django 2.1.5 on 2019-02-16 21:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='主题')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='结束时间')),
                ('credit', models.FloatField(choices=[(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (5.5, 5.5), (6.0, 6.0), (6.5, 6.5), (7.0, 7.0), (7.5, 7.5), (8.0, 8.0), (8.5, 8.5), (9.0, 9.0), (9.5, 9.5), (10.0, 10.0), (10.5, 10.5), (11.0, 11.0), (11.5, 11.5), (12.0, 12.0), (12.5, 12.5), (13.0, 13.0), (13.5, 13.5), (14.0, 14.0), (14.5, 14.5), (15.0, 15.0), (15.5, 15.5), (16.0, 16.0), (16.5, 16.5), (17.0, 17.0), (17.5, 17.5), (18.0, 18.0), (18.5, 18.5), (19.0, 19.0), (19.5, 19.5), (20.0, 20.0)], default=0, verbose_name='学时数')),
                ('visualable_others', models.BooleanField(default=False, verbose_name='其他支部可见')),
                ('branch', models.ManyToManyField(to='info.Branch', verbose_name='主/承办党支部')),
            ],
            options={
                'verbose_name': '会议/活动',
                'verbose_name_plural': '会议/活动',
                'ordering': ('-date', 'name'),
            },
        ),
        migrations.CreateModel(
            name='TakePartIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(null=True, verbose_name='结束时间')),
                ('credit', models.FloatField(choices=[(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (5.5, 5.5), (6.0, 6.0), (6.5, 6.5), (7.0, 7.0), (7.5, 7.5), (8.0, 8.0), (8.5, 8.5), (9.0, 9.0), (9.5, 9.5), (10.0, 10.0), (10.5, 10.5), (11.0, 11.0), (11.5, 11.5), (12.0, 12.0), (12.5, 12.5), (13.0, 13.0), (13.5, 13.5), (14.0, 14.0), (14.5, 14.5), (15.0, 15.0), (15.5, 15.5), (16.0, 16.0), (16.5, 16.5), (17.0, 17.0), (17.5, 17.5), (18.0, 18.0), (18.5, 18.5), (19.0, 19.0), (19.5, 19.5), (20.0, 20.0)], default=0, null=True, verbose_name='学时数')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teaching.Activity', verbose_name='党建活动')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Member', verbose_name='支部成员')),
            ],
            options={
                'verbose_name': '学时统计',
                'verbose_name_plural': '学时统计',
                'ordering': ('activity', 'member'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='takepartin',
            unique_together={('activity', 'member')},
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together={('name', 'date')},
        ),
    ]
