from django.db import models
# Create your models here.


class NullableDateField(models.DateField):
    def __init__(self, verbose_name=None, name=None, auto_now=False, auto_now_add=False, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['max_length'] = 10
        kwargs['default'] = None
        super().__init__(verbose_name, name, auto_now, auto_now_add, **kwargs)


class Branch(models.Model):
    branch_name = models.CharField('组织名称', unique=True, max_length=50)
    date_create = NullableDateField('成立日期')

    class Meta:
        ordering = ('branch_name', )
        verbose_name = '基层组织'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.branch_name


class Member(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='支部')
    netid = models.CharField('学号', max_length=8, primary_key=True)
    name = models.CharField('姓名', max_length=20, db_index=True)
    birth_date = models.DateField(max_length=10, verbose_name='出生时间')
    gender = models.CharField(max_length=1, verbose_name='性别', choices=[('男', '男'), ('女', '女')], default='男')
    group = models.CharField(max_length=20, verbose_name='民族')
    place_birth = models.CharField(max_length=50, verbose_name='籍贯')
    major_in = models.CharField(max_length=30, verbose_name='当前专业（全称）')

    youth_league_date = NullableDateField(verbose_name='加入共青团')
    constitution_group_date = NullableDateField(verbose_name='参加党章学习小组')
    application_date = NullableDateField(verbose_name='递交入党申请书')
    activist_date = NullableDateField('确定为入党积极分子')
    league_promotion_date = NullableDateField(verbose_name='团支部推优（重点发展对象）')
    democratic_appraisal_date = NullableDateField(verbose_name='民主评议')
    political_check_date = NullableDateField(verbose_name='政治审查')
    key_develop_person_date = NullableDateField(verbose_name='确认为重点发展对象')
    graduated_party_school_date = NullableDateField(verbose_name='党校培训结业')

    recommenders_date = NullableDateField(verbose_name='确认入党介绍人')
    recommenders = models.CharField(max_length=50, null=True, blank=True, verbose_name='入党介绍人')
    autobiography_date = NullableDateField(verbose_name='填写自传')
    application_form_date = NullableDateField(verbose_name='填写入党志愿书')
    first_branch_conference = NullableDateField(verbose_name='支部大会通过成为预备党员')
    pro_conversation_date = NullableDateField(verbose_name='入党谈话')
    talker = models.CharField(max_length=50, null=True, blank=True, verbose_name='入党谈话人')
    probationary_approval_date = NullableDateField(verbose_name='党委批准成为预备党员')
    oach_date = NullableDateField(verbose_name='入党宣誓')

    application_fullmember_date = NullableDateField(verbose_name='递交转正申请书')
    second_branch_conference = NullableDateField(verbose_name='支部大会通过成为正式党员')
    fullmember_approval_date = NullableDateField(verbose_name='党委批准成为正式党员')

    class Meta:
        ordering = ('branch', 'netid', )
        verbose_name = '成员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.branch.branch_name + ' ' + self.name

    def important_dates(self):
        return [(field.verbose_name, getattr(self, field.name)) for field in self._meta.fields
                if field.name != 'birth_date' and isinstance(field, models.DateField)]
