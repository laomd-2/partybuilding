# Generated by Django 2.1.7 on 2019-02-28 11:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20190228_1137'),
        ('teaching', '0002_activity_atv_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sharing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=100, null=True)),
                ('impression', models.CharField(max_length=200, null=True)),
                ('added', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Member')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='cascade',
            field=models.BooleanField(default=False, help_text='当会议/活动的学时数改变时，自动在学时统计中更新。', verbose_name='级联更新'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='credit',
            field=models.FloatField(choices=[(0.0, 0.0), (0.1, 0.1), (0.2, 0.2), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (5.5, 5.5), (6.0, 6.0), (6.5, 6.5), (7.0, 7.0), (7.5, 7.5), (8.0, 8.0), (8.5, 8.5), (9.0, 9.0), (9.5, 9.5), (10.0, 10.0), (10.5, 10.5), (11.0, 11.0), (11.5, 11.5), (12.0, 12.0), (12.5, 12.5), (13.0, 13.0), (13.5, 13.5), (14.0, 14.0), (14.5, 14.5), (15.0, 15.0), (15.5, 15.5), (16.0, 16.0), (16.5, 16.5), (17.0, 17.0), (17.5, 17.5), (18.0, 18.0), (18.5, 18.5), (19.0, 19.0), (19.5, 19.5), (20.0, 20.0)], default=0, verbose_name='学时数'),
        ),
        migrations.AlterField(
            model_name='takepartin',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teaching.Activity', verbose_name='会议/活动'),
        ),
        migrations.AlterField(
            model_name='takepartin',
            name='credit',
            field=models.FloatField(default=0, null=True, verbose_name='学时数'),
        ),
    ]