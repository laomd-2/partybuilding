# Generated by Django 2.1.7 on 2019-05-15 16:19

from django.db import migrations, models
import django.db.models.deletion
import info.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=50, verbose_name='名称')),
                ('date_create', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='成立日期')),
            ],
            options={
                'verbose_name': '组织管理',
                'verbose_name_plural': '组织管理',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_1', models.CharField(choices=[('birth_date', '出生时间'), ('constitution_group_date', '参加党章学习小组时间'), ('application_date', '递交入党申请书时间'), ('first_talk_date', '首次组织谈话时间'), ('activist_date', '确定为入党积极分子时间'), ('democratic_appraisal_date', '民主评议时间'), ('league_promotion_date', '推荐/推优时间'), ('key_develop_meeting_date', '支部大会讨论确定发展对象时间'), ('key_develop_person_date', '确定发展对象时间'), ('graduated_party_school_date', '党校培训结业时间'), ('probationary_pre_date', '党委预审时间'), ('recommenders_date', '确定入党介绍人时间'), ('first_branch_conference', '确定为预备党员时间'), ('pro_conversation_date', '入党谈话时间'), ('probationary_approval_date', '党委审批时间'), ('oach_date', '入党宣誓时间'), ('application_fullmember_date', '递交转正申请书时间'), ('second_branch_conference', '转正时间'), ('fullmember_approval_date', '党委审批时间2'), ('archive_date', '转档案馆时间'), ('reserve_party_member_date', '申请保留党籍时间'), ('out_date', '关系转出时间')], max_length=50, verbose_name='从')),
                ('to', models.CharField(choices=[('birth_date', '出生时间'), ('constitution_group_date', '参加党章学习小组时间'), ('application_date', '递交入党申请书时间'), ('first_talk_date', '首次组织谈话时间'), ('activist_date', '确定为入党积极分子时间'), ('democratic_appraisal_date', '民主评议时间'), ('league_promotion_date', '推荐/推优时间'), ('key_develop_meeting_date', '支部大会讨论确定发展对象时间'), ('key_develop_person_date', '确定发展对象时间'), ('graduated_party_school_date', '党校培训结业时间'), ('probationary_pre_date', '党委预审时间'), ('recommenders_date', '确定入党介绍人时间'), ('first_branch_conference', '确定为预备党员时间'), ('pro_conversation_date', '入党谈话时间'), ('probationary_approval_date', '党委审批时间'), ('oach_date', '入党宣誓时间'), ('application_fullmember_date', '递交转正申请书时间'), ('second_branch_conference', '转正时间'), ('fullmember_approval_date', '党委审批时间2'), ('archive_date', '转档案馆时间'), ('reserve_party_member_date', '申请保留党籍时间'), ('out_date', '关系转出时间')], max_length=50, verbose_name='到')),
                ('days', models.IntegerField(choices=[(30, '1个月'), (60, '2个月'), (90, '3个月'), (180, '半年'), (365, '1年'), (6570, '18年'), (1, '1天'), (2, '2天'), (3, '3天'), (4, '4天'), (5, '5天'), (6, '6天'), (7, '7天'), (8, '8天'), (9, '9天'), (10, '10天')], verbose_name='周期')),
                ('scope', models.IntegerField(choices=[(0, '全部'), (1, '中大发展党员'), (2, '非中大发展党员')], default=0, verbose_name='适用范围')),
            ],
            options={
                'verbose_name': '流程依赖',
                'verbose_name_plural': '流程依赖',
                'ordering': ('from_1', 'to', 'days'),
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('netid', models.IntegerField(primary_key=True, serialize=False, verbose_name='学号')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='姓名')),
                ('birth_date', models.DateField(max_length=10, verbose_name='出生时间')),
                ('gender', models.CharField(choices=[('男', '男'), ('女', '女')], default='男', max_length=1, verbose_name='性别')),
                ('group', models.CharField(default='汉', max_length=20, verbose_name='民族')),
                ('jiguan', models.CharField(blank=True, max_length=50, null=True, verbose_name='籍贯')),
                ('family_address', models.CharField(blank=True, max_length=50, null=True, verbose_name='家庭住址')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='在前面加上+86', max_length=128, null=True, region=None, verbose_name='联系电话')),
                ('id_card_number', models.CharField(blank=True, help_text='18位，除最后一位可以是x或X外，其他17位是数字。出生日期和性别需要对应。', max_length=20, null=True, verbose_name='身份证号码')),
                ('major_in', models.CharField(blank=True, help_text='填写当前所在专业的全称。', max_length=30, null=True, verbose_name='当前专业')),
                ('years', models.IntegerField(default=4, help_text='延期毕业可以增加学年制。', verbose_name='学年制')),
                ('youth_league_member', models.BooleanField(default=True, verbose_name='是否团员')),
                ('constitution_group_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='参加党章学习小组时间')),
                ('is_sysu', models.BooleanField(default=True, help_text='在中山大学发展的党员，其录入的信息需严格遵循相关流程依赖。', verbose_name='是否在中山大学发展')),
                ('application_date', info.models.NullableDateField(blank=True, default=None, help_text='与入党申请书落款时间一致，需保证年满18周岁。', max_length=10, null=True, verbose_name='递交入党申请书时间')),
                ('first_talk_date', info.models.NullableDateField(blank=True, default=None, help_text='党支部收到入党申请书后，一个月内委派支委与其谈话的时间。', max_length=10, null=True, verbose_name='首次组织谈话时间')),
                ('activist_date', info.models.NullableDateField(blank=True, default=None, help_text='党支部开会讨论，通过成为入党积极分子的时间。', max_length=10, null=True, verbose_name='确定为入党积极分子时间')),
                ('democratic_appraisal_date', info.models.NullableDateField(blank=True, default=None, help_text='党支部召开座谈会收集群众意见的时间。', max_length=10, null=True, verbose_name='民主评议时间')),
                ('league_promotion_date', info.models.NullableDateField(blank=True, default=None, help_text='非团员采用党员推荐的方式，团员采用团支部推优的方式。', max_length=10, null=True, verbose_name='推荐/推优时间')),
                ('key_develop_meeting_date', info.models.NullableDateField(blank=True, default=None, help_text='党支部开会时间。', max_length=10, null=True, verbose_name='支部大会讨论确定发展对象时间')),
                ('key_develop_person_date', info.models.NullableDateField(blank=True, default=None, help_text='上级党委备案时间。', max_length=10, null=True, verbose_name='确定发展对象时间')),
                ('is_political_check', models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20, verbose_name='政治审查')),
                ('graduated_party_school_date', info.models.NullableDateField(blank=True, default=None, help_text='未通过则不填写。', max_length=10, null=True, verbose_name='党校培训结业时间')),
                ('probationary_pre_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='党委预审时间')),
                ('recommenders_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='确定入党介绍人时间')),
                ('recommenders', models.CharField(blank=True, help_text='两名正式党员。', max_length=50, null=True, verbose_name='入党介绍人')),
                ('autobiography', models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20, verbose_name='自传')),
                ('application_form', models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20, verbose_name='入党志愿书')),
                ('first_branch_conference', info.models.NullableDateField(blank=True, default=None, help_text='支部党员大会通过成为预备党员的时间。', max_length=10, null=True, verbose_name='确定为预备党员时间')),
                ('pro_conversation_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='入党谈话时间')),
                ('talker', models.CharField(blank=True, help_text='学院党委成员或组织员。', max_length=50, null=True, verbose_name='入党谈话人')),
                ('probationary_approval_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='党委审批时间')),
                ('oach_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='入党宣誓时间')),
                ('application_fullmember_date', info.models.NullableDateField(blank=True, default=None, help_text='预备党员应提前一个月向党支部递交。', max_length=10, null=True, verbose_name='递交转正申请书时间')),
                ('second_branch_conference', info.models.NullableDateField(blank=True, default=None, help_text='支部大会讨论转正时间。', max_length=10, null=True, verbose_name='转正时间')),
                ('fullmember_approval_date', info.models.NullableDateField(blank=True, default=None, help_text='正式党员党委审批时间。', max_length=10, null=True, verbose_name='党委审批时间2')),
                ('archive_date', info.models.NullableDateField(blank=True, default=None, help_text='临近毕业时，整理党员资料移交到档案馆。', max_length=10, null=True, verbose_name='转档案馆时间')),
                ('reserve_party_member_date', info.models.NullableDateField(blank=True, default=None, help_text='出国留学人员填写', max_length=10, null=True, verbose_name='申请保留党籍时间')),
                ('out_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='关系转出时间')),
                ('out_place', models.CharField(blank=True, max_length=50, null=True, verbose_name='转出单位')),
                ('remarks', models.TextField(blank=True, help_text='填写各阶段延期发展的原因，或其他重要信息。', null=True, verbose_name='备注')),
                ('phase', models.IntegerField(choices=[(1, '提交入党申请'), (2, '积极分子'), (3, '发展对象'), (4, '预备党员'), (5, '正式党员')], default=1, editable=False, verbose_name='发展阶段')),
                ('branch', models.ForeignKey(on_delete=models.SET(1), to='info.Branch', verbose_name='党支部名称')),
            ],
            options={
                'verbose_name': '党员发展管理',
                'verbose_name_plural': '党员发展管理',
                'ordering': ('branch', 'netid'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OldMember',
            fields=[
                ('netid', models.IntegerField(primary_key=True, serialize=False, verbose_name='学号')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='姓名')),
                ('birth_date', models.DateField(max_length=10, verbose_name='出生时间')),
                ('gender', models.CharField(choices=[('男', '男'), ('女', '女')], default='男', max_length=1, verbose_name='性别')),
                ('group', models.CharField(default='汉', max_length=20, verbose_name='民族')),
                ('jiguan', models.CharField(blank=True, max_length=50, null=True, verbose_name='籍贯')),
                ('family_address', models.CharField(blank=True, max_length=50, null=True, verbose_name='家庭住址')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='在前面加上+86', max_length=128, null=True, region=None, verbose_name='联系电话')),
                ('id_card_number', models.CharField(blank=True, help_text='18位，除最后一位可以是x或X外，其他17位是数字。出生日期和性别需要对应。', max_length=20, null=True, verbose_name='身份证号码')),
                ('major_in', models.CharField(blank=True, help_text='填写当前所在专业的全称。', max_length=30, null=True, verbose_name='当前专业')),
                ('years', models.IntegerField(default=4, help_text='延期毕业可以增加学年制。', verbose_name='学年制')),
                ('youth_league_member', models.BooleanField(default=True, verbose_name='是否团员')),
                ('constitution_group_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='参加党章学习小组时间')),
                ('is_sysu', models.BooleanField(default=True, help_text='在中山大学发展的党员，其录入的信息需严格遵循相关流程依赖。', verbose_name='是否在中山大学发展')),
                ('application_date', info.models.NullableDateField(blank=True, default=None, help_text='与入党申请书落款时间一致，需保证年满18周岁。', max_length=10, null=True, verbose_name='递交入党申请书时间')),
                ('first_talk_date', info.models.NullableDateField(blank=True, default=None, help_text='党支部收到入党申请书后，一个月内委派支委与其谈话的时间。', max_length=10, null=True, verbose_name='首次组织谈话时间')),
                ('activist_date', info.models.NullableDateField(blank=True, default=None, help_text='党支部开会讨论，通过成为入党积极分子的时间。', max_length=10, null=True, verbose_name='确定为入党积极分子时间')),
                ('democratic_appraisal_date', info.models.NullableDateField(blank=True, default=None, help_text='党支部召开座谈会收集群众意见的时间。', max_length=10, null=True, verbose_name='民主评议时间')),
                ('league_promotion_date', info.models.NullableDateField(blank=True, default=None, help_text='非团员采用党员推荐的方式，团员采用团支部推优的方式。', max_length=10, null=True, verbose_name='推荐/推优时间')),
                ('key_develop_meeting_date', info.models.NullableDateField(blank=True, default=None, help_text='党支部开会时间。', max_length=10, null=True, verbose_name='支部大会讨论确定发展对象时间')),
                ('key_develop_person_date', info.models.NullableDateField(blank=True, default=None, help_text='上级党委备案时间。', max_length=10, null=True, verbose_name='确定发展对象时间')),
                ('is_political_check', models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20, verbose_name='政治审查')),
                ('graduated_party_school_date', info.models.NullableDateField(blank=True, default=None, help_text='未通过则不填写。', max_length=10, null=True, verbose_name='党校培训结业时间')),
                ('probationary_pre_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='党委预审时间')),
                ('recommenders_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='确定入党介绍人时间')),
                ('recommenders', models.CharField(blank=True, help_text='两名正式党员。', max_length=50, null=True, verbose_name='入党介绍人')),
                ('autobiography', models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20, verbose_name='自传')),
                ('application_form', models.CharField(choices=[('完成', '完成'), ('未完成', '未完成')], default='未完成', max_length=20, verbose_name='入党志愿书')),
                ('first_branch_conference', info.models.NullableDateField(blank=True, default=None, help_text='支部党员大会通过成为预备党员的时间。', max_length=10, null=True, verbose_name='确定为预备党员时间')),
                ('pro_conversation_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='入党谈话时间')),
                ('talker', models.CharField(blank=True, help_text='学院党委成员或组织员。', max_length=50, null=True, verbose_name='入党谈话人')),
                ('probationary_approval_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='党委审批时间')),
                ('oach_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='入党宣誓时间')),
                ('application_fullmember_date', info.models.NullableDateField(blank=True, default=None, help_text='预备党员应提前一个月向党支部递交。', max_length=10, null=True, verbose_name='递交转正申请书时间')),
                ('second_branch_conference', info.models.NullableDateField(blank=True, default=None, help_text='支部大会讨论转正时间。', max_length=10, null=True, verbose_name='转正时间')),
                ('fullmember_approval_date', info.models.NullableDateField(blank=True, default=None, help_text='正式党员党委审批时间。', max_length=10, null=True, verbose_name='党委审批时间2')),
                ('archive_date', info.models.NullableDateField(blank=True, default=None, help_text='临近毕业时，整理党员资料移交到档案馆。', max_length=10, null=True, verbose_name='转档案馆时间')),
                ('reserve_party_member_date', info.models.NullableDateField(blank=True, default=None, help_text='出国留学人员填写', max_length=10, null=True, verbose_name='申请保留党籍时间')),
                ('out_date', info.models.NullableDateField(blank=True, default=None, max_length=10, null=True, verbose_name='关系转出时间')),
                ('out_place', models.CharField(blank=True, max_length=50, null=True, verbose_name='转出单位')),
                ('remarks', models.TextField(blank=True, help_text='填写各阶段延期发展的原因，或其他重要信息。', null=True, verbose_name='备注')),
                ('phase', models.IntegerField(choices=[(1, '提交入党申请'), (2, '积极分子'), (3, '发展对象'), (4, '预备党员'), (5, '正式党员')], default=1, editable=False, verbose_name='发展阶段')),
                ('branch', models.ForeignKey(on_delete=models.SET(1), to='info.Branch', verbose_name='党支部名称')),
            ],
            options={
                'verbose_name': '历史党员管理',
                'verbose_name_plural': '历史党员管理',
                'ordering': ('branch', 'netid'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='名称')),
            ],
            options={
                'verbose_name': '学院',
                'verbose_name_plural': '学院',
                'ordering': ('name',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='dependency',
            unique_together={('from_1', 'to', 'scope')},
        ),
        migrations.AddField(
            model_name='branch',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.School', verbose_name='学院'),
        ),
    ]
