# Generated by Django 2.1.7 on 2019-05-09 20:08

from django.db import migrations, models
import info.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ('info', '0004_auto_20190508_2222'),
    ]

    operations = [

        migrations.AddField(
            model_name='member',
            name='application_form',
            field=models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20,
                                   verbose_name='入党志愿书'),
        ),
        migrations.AddField(
            model_name='member',
            name='autobiography',
            field=models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20,
                                   verbose_name='自传'),
        ),
        migrations.AddField(
            model_name='member',
            name='is_political_check',
            field=models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20,
                                   verbose_name='政治审查'),
        ),
        migrations.AddField(
            model_name='member',
            name='jiguan',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='籍贯'),
        ),
        migrations.AddField(
            model_name='member',
            name='key_develop_meeting_date',
            field=info.models.NullableDateField(blank=True, default=None, max_length=10, null=True,
                                                verbose_name='支部大会讨论确定发展对象时间'),
        ),
        migrations.AddField(
            model_name='member',
            name='probationary_pre_date',
            field=info.models.NullableDateField(blank=True, default=None, max_length=10, null=True,
                                                verbose_name='党委预审时间'),
        ),
        migrations.AddField(
            model_name='member',
            name='reserve_party_member_date',
            field=info.models.NullableDateField(blank=True, default=None, help_text='出国留学人员填写', max_length=10,
                                                null=True, verbose_name='申请保留党籍时间'),
        )
    ]