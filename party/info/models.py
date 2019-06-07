import datetime
from copy import copy
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import smart_str
from phonenumber_field.modelfields import PhoneNumberField
from collections import OrderedDict
from common.utils import Cache
from common.models import MyBooleanField
from django.db.models.signals import post_delete
from django.dispatch import receiver


def get_branch_managers():
    group = Group.objects.get(name='党支部管理员')
    managers = group.user_set.all().prefetch_related('group').values('username', 'email')
    branch_managers = dict()
    for manager in managers:
        try:
            member = Member.objects.filter(netid=int(manager['username'])).extra(select={
                'branch_name': 'info_branch.branch_name'
            }).values('branch_name', 'name')[0]
            branch_managers.setdefault(member['branch_name'], [])
            manager['name'] = member['name']
            branch_managers[member['branch_name']].append(manager)
        except IndexError:
            pass
    return branch_managers


class NullableDateField(models.DateField):
    def __init__(self, verbose_name=None, name=None, auto_now=False, auto_now_add=False, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['max_length'] = 10
        kwargs['default'] = None
        super().__init__(verbose_name, name, auto_now, auto_now_add, **kwargs)


class School(models.Model):
    name = models.CharField('名称', unique=True, max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = '学院'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Branch(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='学院')
    branch_name = models.CharField('名称', max_length=50)
    date_create = NullableDateField('成立日期')

    class Meta:
        ordering = ('id',)
        verbose_name = '组织管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.branch_name

    def validate_unique(self, exclude=None):
        qs = Branch.objects.filter(school=self.school)
        if self.pk is None:
            if qs.filter(branch_name=self.branch_name).exists():
                raise ValidationError("%s的%s已存在。" % (self.school, self.branch_name))

    @property
    def qs(self):
        if self.id == 6:
            qs = Member.objects
        else:
            qs = self.member_set
        return qs

    def num_members(self):
        return self.qs.count()

    num_members.short_description = '成员数'

    def num_full_members(self):
        return self.qs.filter(second_branch_conference__isnull=False).count()

    num_full_members.short_description = '正式党员'

    def num_pre_members(self):
        return self.qs.filter(first_branch_conference__isnull=False,
                              second_branch_conference__isnull=True).count()

    num_pre_members.short_description = '预备党员'

    def num_key(self):
        return self.qs.filter(key_develop_person_date__isnull=False,
                              first_branch_conference__isnull=True).count()

    num_key.short_description = '重点发展对象'

    def num_activist(self):
        return self.qs.filter(activist_date__isnull=False, key_develop_person_date__isnull=True).count()

    num_activist.short_description = '积极分子'

    def num_application(self):
        return self.qs.filter(application_date__isnull=False, activist_date__isnull=True).count()

    num_application.short_description = '申请人员'

    leader_cache = Cache(5)

    @staticmethod
    def branch_leaders():
        leaders = Branch.leader_cache.get()
        if leaders is None:
            leaders = get_branch_managers()
            Branch.leader_cache.set(leaders)
        return leaders

    def get_leaders(self):
        managers = self.branch_leaders().get(self.branch_name, [])
        members = list(map(lambda x: x['name'], managers))
        return ','.join(members) if members else '无'

    get_leaders.short_description = '支部委员'


def upload_to(instance, filename):
    return 'info/' + str(instance.netid) + '/' + smart_str(filename)


@receiver(post_delete)
def delete_member(sender, instance, **kwargs):
    if issubclass(sender, MemberBase):
        if instance.branch_id != 106:
            instance = copy(instance)
            instance.branch_id = 106
            instance.save(ignore_check=True)


class MemberBaseManager(models.Manager):

    def all(self):
        return super().all().exclude(branch_id=106)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs).exclude(branch_id=106)


class MemberBase(models.Model):
    phases = [
        (1, '提交入党申请'), (2, '积极分子'), (3, '发展对象'), (4, '预备党员'), (5, '正式党员')
    ]

    branch = models.ForeignKey(Branch, on_delete=models.SET(106), verbose_name='党支部名称', db_index=True)
    netid = models.IntegerField('学号', primary_key=True)
    name = models.CharField('姓名', max_length=20, db_index=True)
    birth_date = models.DateField(max_length=10, verbose_name='出生时间')
    gender = models.CharField(max_length=1, verbose_name='性别', choices=[('男', '男'), ('女', '女')], default='男')
    group = models.CharField(max_length=20, verbose_name='民族', default='汉')
    jiguan = models.CharField(max_length=50, verbose_name='籍贯', null=True, blank=True)
    family_address = models.CharField(max_length=50, verbose_name='家庭住址', null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name='联系电话', null=True, blank=True, help_text='在前面加上+86')
    id_card_number = models.CharField(max_length=20, verbose_name='身份证号码', null=True, blank=True,
                                      help_text='18位，除最后一位可以是x或X外，其他17位是数字。出生日期和性别需要对应。')
    major_in = models.CharField(max_length=30, verbose_name='当前专业', null=True, blank=True,
                                help_text='填写当前所在专业的全称。')
    years = models.IntegerField('学年制', default=4, help_text='转专业或休学时可以增加学年制。')
    youth_league_member = MyBooleanField(verbose_name='是否团员', default=True, help_text='非团员发展时采用党员推荐方式。')
    constitution_group_date = NullableDateField(verbose_name='参加党章学习小组时间')
    is_sysu = MyBooleanField(verbose_name='是否在中山大学发展', help_text='在中山大学发展的党员，其录入的信息需严格遵循'
                                                                 '相关流程依赖。', default=True)

    application_date = NullableDateField(verbose_name='递交入党申请书时间', help_text='与入党申请书落款时间一致，需保证年满18周岁。')
    first_talk_date = NullableDateField(verbose_name='首次组织谈话时间', help_text='党支部收到入党申请书后，一个月内委派支委与其谈话的时间。')

    activist_date = NullableDateField('确定为入党积极分子时间', help_text='党支部开会讨论，通过成为入党积极分子的时间。')
    democratic_appraisal_date = NullableDateField(verbose_name='民主评议时间', help_text='党支部召开座谈会收集群众意见的时间。')
    league_promotion_date = NullableDateField(verbose_name='推荐/推优时间', help_text='非团员采用党员推荐的方式，团员采用团支部推优的方式。')
    key_develop_meeting_date = NullableDateField('支部大会讨论确定发展对象时间', help_text='党支部开会时间。')
    key_develop_person_date = NullableDateField(verbose_name='确定发展对象时间', help_text='上级党委备案时间。')
    is_political_check = models.CharField(verbose_name='政治审查', max_length=20, choices=[
        ('完成', '完成'), ('未完成', '未完成')
    ], default='未完成')
    graduated_party_school_date = NullableDateField(verbose_name='党校培训结业时间', help_text='未通过则不填写。')

    probationary_pre_date = NullableDateField('党委预审时间')
    recommenders_date = NullableDateField(verbose_name='确定入党介绍人时间')
    recommenders = models.CharField(max_length=50, null=True, blank=True, verbose_name='入党介绍人',
                                    help_text='两名正式党员。')
    autobiography = models.CharField(verbose_name='自传', max_length=20, choices=[
        ('完成', '完成'), ('未完成', '未完成')
    ], default='未完成')
    application_form = models.CharField(verbose_name='入党志愿书', max_length=20, choices=[
        ('完成', '完成'), ('未完成', '未完成')
    ], default='未完成')
    first_branch_conference = NullableDateField(verbose_name='确定为预备党员时间', help_text='支部党员大会通过成为预备党员的时间。')
    pro_conversation_date = NullableDateField(verbose_name='入党谈话时间')
    talker = models.CharField(max_length=50, null=True, blank=True, verbose_name='入党谈话人', help_text='学院党委成员或组织员。')
    probationary_approval_date = NullableDateField(verbose_name='党委审批时间')
    oach_date = NullableDateField(verbose_name='入党宣誓时间')

    application_fullmember_date = NullableDateField(verbose_name='递交转正申请书时间', help_text='预备党员应提前一个月向党支部递交。')
    second_branch_conference = NullableDateField(verbose_name='转正时间', help_text='支部大会讨论转正时间。')
    fullmember_approval_date = NullableDateField(verbose_name='党委审批时间2', help_text='正式党员党委审批时间。')
    archive_date = NullableDateField('转档案馆时间', help_text='临近毕业时，整理党员资料移交到档案馆。')
    reserve_party_member_date = NullableDateField('申请保留党籍时间', help_text='出国留学人员填写')

    out_date = NullableDateField('关系转出时间')
    out_type = models.CharField('转出类型', null=True, blank=True, max_length=20, choices=[
        (c, c) for c in ['C.出国境升学', 'D.就业', 'E.暂缓就业', 'F.延毕', 'G.境内升学', 'Z.无']
    ])
    out_place = models.CharField('去向单位', blank=True, null=True, max_length=50)
    remarks = models.TextField('备注', blank=True, null=True, help_text='填写各阶段延期发展的原因，或其他重要信息。')

    phase = models.IntegerField('发展阶段', choices=phases, default=1, editable=False)

    class Meta:
        ordering = ('branch', 'netid',)
        abstract = True

    objects = MemberBaseManager()

    def __str__(self):
        return ('%s(%d)' % (self.name, self.netid)) if self.netid is not None else self.name

    def is_party_member(self):
        return self.is_pre_party_member() or self.is_real_party_member()

    def is_pre_party_member(self):
        return self.first_branch_conference

    def is_real_party_member(self):
        return self.second_branch_conference

    def first_talk_end(self):
        return self.application_date + datetime.timedelta(days=30)

    first_talk_end.short_description = '谈话截止时间'

    def grade(self):
        return "20%s" % str(self.netid)[:2]

    grade.short_description = '年级'

    def write_application_date_end(self):
        return self.first_branch_conference + datetime.timedelta(days=365 - 31)

    write_application_date_end.short_description = '转正申请截止时间'

    @staticmethod
    def get_phases():
        fenge = OrderedDict([
            ('application_date', '基本信息'),
            ('activist_date', '入党申请阶段'),
            ('probationary_pre_date', '积极分子和发展对象确定和考察阶段'),
            ('application_fullmember_date', '预备党员'),
            ('out_date', '正式党员')])
        phases = dict()
        last = 0
        fields_ = [field.name for field in MemberBase._meta.fields]
        for k, v in fenge.items():
            if k:
                tmp = fields_.index(k)
            else:
                tmp = -1
            phases[v] = fields_[last: tmp]
            last = tmp
        return fields_, phases

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.phone_number and not str(self.phone_number).startswith('+86'):
            self.phone_number = '+86' + self.phone_number
        super().save(force_insert, force_update, using, update_fields)


class Member(MemberBase):
    class Meta(MemberBase.Meta):
        verbose_name = '党员发展管理'
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, ignore_check=False):
        if self.out_type != 'Z.无' and self.out_place:
            if self.out_type == 'D.就业' or self.out_type == 'G.境内升学':  # mysql视图自动保存到历史党员中
                self.out_date = datetime.date.today()
            elif self.out_type == 'C.出国境升学':
                self.out_date = datetime.date.today()
                try:
                    abroad_branch = Branch.objects.filter(branch_name='出国留学党支部').values('id')[0]['id']
                except IndexError:
                    try:
                        abroad_branch = Branch.objects.filter(branch_name='临时党支部').values('id')[0]['id']
                    except IndexError:
                        abroad_branch = None
                if abroad_branch is not None:
                    self.branch_id = abroad_branch
        super().save(force_insert, force_update, using, update_fields)

    def get_identity(self):
        if self.second_branch_conference:
            return '正式党员'
        if self.first_branch_conference:
            return '预备党员'
        if self.key_develop_person_date:
            return '重点发展对象'
        if self.activist_date:
            return '入党积极分子'
        if self.application_date:
            return '入党申请人'
        return '无'

    get_identity.short_description = '阶段'


class OldMember(MemberBase):
    class Meta(MemberBase.Meta):
        verbose_name = '历史党员管理'
        verbose_name_plural = verbose_name


class Dependency(models.Model):
    all_dates = {f.name: f.verbose_name for f in MemberBase._meta.fields if isinstance(f, models.DateField)}
    days_mapping = dict([(30, '1个月'), (60, '2个月'),
                         (90, '3个月'), (180, '半年'),
                         (365, '1年'), (18 * 365, '18年')] +
                        [(d + 1, "%d天" % (d + 1)) for d in range(10)])
    from_1 = models.CharField('从', choices=all_dates.items(), max_length=50)
    to = models.CharField('到', choices=all_dates.items(), max_length=50)
    days = models.IntegerField('周期', choices=days_mapping.items())
    scope = models.IntegerField('适用范围', choices=[(0, '全部'), (1, '中大发展党员'), (2, '非中大发展党员')], default=0)

    class Meta:
        unique_together = ('from_1', 'to', 'scope')
        ordering = ('from_1', 'to', 'days')
        verbose_name = '流程依赖'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s→%s: %s" % (self.all_dates[self.from_1], self.all_dates[self.to],
                              self.days_mapping[self.days])
