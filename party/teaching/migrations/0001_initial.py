# Generated by Django 2.1.7 on 2019-05-15 16:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import teaching.models


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
                ('name', models.CharField(max_length=100, verbose_name='活动主题')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='开展时间')),
                ('atv_type', models.CharField(choices=[('主题党日/党课', '主题党日/党课'), ('讲座/培训', '讲座/培训'), ('其他', '其他')], max_length=10, verbose_name='活动类型')),
                ('credit', models.FloatField(default=0, verbose_name='学时数')),
                ('cascade', models.BooleanField(default=False, help_text='当会议/活动的学时数改变时，自动在学时统计中更新。', verbose_name='级联更新')),
                ('visualable_others', models.BooleanField(default=False, help_text='是否向其他支部公开。', verbose_name='公开')),
                ('checkin_code', models.IntegerField(blank=True, null=True, verbose_name='签到码')),
                ('checkin_qr', teaching.models.NullableImageField(blank=True, editable=False, null=True, upload_to=teaching.models.upload_to, verbose_name='签到二维码')),
                ('branch', models.ManyToManyField(to='info.Branch', verbose_name='主办单位/党支部')),
            ],
            options={
                'verbose_name': '会议和活动',
                'verbose_name_plural': '会议和活动',
                'ordering': ('-date', 'name'),
            },
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.IntegerField()),
                ('netid', models.IntegerField()),
                ('ip', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sharing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(default=django.utils.timezone.now, verbose_name='时间')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='标题')),
                ('impression', models.TextField(default='', verbose_name='学习心得')),
                ('added', models.BooleanField(default=False, verbose_name='审核通过')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Member', verbose_name='支部成员')),
            ],
            options={
                'verbose_name': '学习打卡',
                'verbose_name_plural': '学习打卡',
                'ordering': ('-when',),
            },
        ),
        migrations.CreateModel(
            name='TakePartIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.FloatField(default=0, null=True, verbose_name='学时数')),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最后修改时间')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teaching.Activity', verbose_name='活动主题')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Member', verbose_name='学号')),
            ],
            options={
                'verbose_name': '党员学时统计',
                'verbose_name_plural': '党员学时统计',
                'ordering': ('member', '-activity'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TakePartIn2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.FloatField(default=0, null=True, verbose_name='学时数')),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最后修改时间')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teaching.Activity', verbose_name='活动主题')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Member', verbose_name='学号')),
            ],
            options={
                'verbose_name': '非党员学时统计',
                'verbose_name_plural': '非党员学时统计',
                'ordering': ('member', '-activity'),
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together={('activity_id', 'netid')},
        ),
        migrations.AlterUniqueTogether(
            name='takepartin2',
            unique_together={('activity', 'member')},
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
