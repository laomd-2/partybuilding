from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from collections import OrderedDict


# Create your models here.


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
        verbose_name = '党支部'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%s)" % (self.branch_name, self.school)

    def validate_unique(self, exclude=None):
        qs = Branch.objects.filter(school=self.school)
        if self.pk is None:
            if qs.filter(branch_name=self.branch_name).exists():
                raise ValidationError("%s的%s已存在。" % (self.school, self.branch_name))


class Member(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='党支部')
    netid = models.IntegerField('学号', primary_key=True)
    name = models.CharField('姓名', max_length=20, db_index=True)
    # identity = models.IntegerField(verbose_name='发展阶段', null=True,
    #                                choices=[(0, '正式党员'), (1, '预备党员'), (2, '重点发展对象'),
    #                                         (3, '入党积极分子'), (4, '入党申请人'), (5, '无')], default=5)
    birth_date = NullableDateField(max_length=10, verbose_name='出生时间')
    gender = models.CharField(max_length=1, verbose_name='性别', choices=[('男', '男'), ('女', '女')], default='男',
                              null=True, blank=True)
    group = models.CharField(max_length=20, verbose_name='民族', null=True, blank=True)
    family_address = models.CharField(max_length=50, verbose_name='家庭住址', null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name='联系电话', null=True, blank=True)
    credit_card_id = models.CharField(verbose_name='身份证号码', null=True, blank=True, max_length=50)
    major_in = models.CharField(max_length=30, verbose_name='当前专业（全称）', null=True, blank=True)

    youth_league_date = NullableDateField(verbose_name='加入共青团时间')
    constitution_group_date = NullableDateField(verbose_name='参加党章学习小组时间')
    application_date = NullableDateField(verbose_name='递交入党申请书时间')
    first_talk_date = NullableDateField(verbose_name='首次组织谈话时间')
    activist_date = NullableDateField('确定为入党积极分子时间')
    league_promotion_date = NullableDateField(verbose_name='团支部推优（重点发展对象）时间')
    democratic_appraisal_date = NullableDateField(verbose_name='民主评议时间')
    political_check_date = NullableDateField(verbose_name='政治审查时间')
    key_develop_person_date = NullableDateField(verbose_name='确定为重点发展对象时间')
    graduated_party_school_date = NullableDateField(verbose_name='党校培训结业时间')

    recommenders_date = NullableDateField(verbose_name='确定入党介绍人时间')
    recommenders = models.CharField(max_length=50, null=True, blank=True, verbose_name='入党介绍人')
    autobiography_date = NullableDateField(verbose_name='填写自传时间')
    application_form_date = NullableDateField(verbose_name='填写入党志愿书时间')
    first_branch_conference = NullableDateField(verbose_name='支部大会通过成为预备党员时间')
    pro_conversation_date = NullableDateField(verbose_name='入党谈话时间')
    talker = models.CharField(max_length=50, null=True, blank=True, verbose_name='入党谈话人')
    probationary_approval_date = NullableDateField(verbose_name='党委批准成为预备党员时间')
    oach_date = NullableDateField(verbose_name='入党宣誓时间')

    application_fullmember_date = NullableDateField(verbose_name='递交转正申请书时间')
    second_branch_conference = NullableDateField(verbose_name='支部大会通过成为正式党员时间')
    fullmember_approval_date = NullableDateField(verbose_name='党委批准成为正式党员时间')

    class Meta:
        ordering = ('branch', 'netid',)
        verbose_name = '成员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.netid) + ' ' + self.name

    def important_dates(self):
        return [(field.verbose_name, getattr(self, field.name)) for field in self._meta.fields
                if field.name != 'birth_date' and isinstance(field, models.DateField)]

    @staticmethod
    def foreign_keys():
        return ['branch']

    @staticmethod
    def export_field_map():
        fields = OrderedDict()
        # fields['党支部ID'] = 'branch'
        for f in Member._meta.fields:
            fields[f.verbose_name + ('ID' if f.name in Member.foreign_keys() else '')] = f.name
        return fields

    @staticmethod
    def necessary_fields():
        fields = list(Member.export_field_map().values())
        fields.remove('identity')
        return fields

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        phases = ['application_date',
                  'activist_date',
                  'key_develop_person_date',
                  'first_branch_conference',
                  'second_branch_conference']
        for i, attr in enumerate(reversed(phases)):
            if getattr(self, attr):
                self.identity = i
                break
        else:
            self.identity = 5
        super().save(force_insert, force_update, using, update_fields)


class Application(models.Model):
    netid = models.IntegerField('学号')
    application_type = models.CharField('申请成为', max_length=20, choices=(
        ('入党申请人', '入党申请'),
        ('入党积极分子', '入党积极分子'),
        ('重点发展对象', '重点发展对象'),
        ('预备党员', '预备党员'),
        ('正式党员', '正式党员')
    ))


class Dependency(models.Model):
    all_dates = {f.name: f.verbose_name for f in Member._meta.fields if isinstance(f, models.DateField)}
    days_mapping = dict([(30, '1个月'), (60, '2个月'),
                         (90, '3个月'), (180, '半年'),
                         (365, '1年'), (18 * 365, '18年')] +
                        [(d + 1, "%d天" % (d + 1)) for d in range(10)])
    from_1 = models.CharField('from', choices=all_dates.items(), max_length=50)
    to = models.CharField('to', choices=all_dates.items(), max_length=50)
    days = models.IntegerField('周期', choices=days_mapping.items())

    class Meta:
        unique_together = ('from_1', 'to')
        ordering = ('from_1', 'to', 'days')
        verbose_name = '发展流程依赖'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s→%s: %s" % (self.all_dates[self.from_1], self.all_dates[self.to],
                              self.days_mapping[self.days])
