import datetime
import os
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from django.utils.encoding import smart_str
import qrcode
import hashlib
from info.models import Member, Branch


def upload_to(instance, filename):
    return Activity._meta.verbose_name + '/' + str(instance) + '/' + smart_str(filename)


def md5(s):
    m = hashlib.md5()
    m.update(str(s).encode('utf-8'))
    return m.hexdigest()


def get_md5id(id, code):
    return md5(id) + md5(code)


def generate_qrcode(activity_id, checkin_code):
    md5_id = get_md5id(activity_id, checkin_code)
    filename = 'qrcode/qrcode%s.png' % md5(md5_id)
    abs_filename = os.path.join(settings.MEDIA_ROOT, filename)
    if not os.path.exists(abs_filename):
        img = qrcode.make(settings.HOST_IP + '/checkin?activity=%d&token=%s' % (activity_id, md5_id))
        with open(abs_filename, 'wb') as f:
            img.save(f)
    return filename


class NullableImageField(models.ImageField):

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        kwargs['upload_to'] = upload_to
        kwargs['null'] = kwargs['blank'] = True
        super().__init__(verbose_name, name, width_field, height_field, **kwargs)


class Phase(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


def get_activity_start_date():
    now = datetime.date.today()
    year, month = now.year, now.month
    if month < 2:
        year -= 1
    return datetime.date(year, 2, 1)


class ActivityManager(models.Manager):
    def all(self):
        return super().all().exclude(date__lt=get_activity_start_date())

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs).exclude(date__lt=get_activity_start_date())


class Activity(models.Model):
    name = models.CharField('活动主题', max_length=100)
    date = models.DateTimeField('开展时间', default=timezone.now)
    # end_time = models.DateTimeField('结束时间', default=timezone.now)
    atv_type_choices = ['主题党日/党课', '讲座/培训', '其他']
    atv_type = models.CharField('活动类型', choices=[
        (t, t) for t in atv_type_choices
    ], max_length=10)
    branch = models.ManyToManyField(Branch, verbose_name='主办单位/党支部')
    credit = models.FloatField('学时数', default=0)
    is_cascade = models.BooleanField('级联更新', default=False, help_text='当会议/活动的学时数改变时，自动在学时统计中更新。')
    visualable_others = models.BooleanField('公开', default=False, help_text='是否向其他支部公开。')

    checkin_code = models.IntegerField(verbose_name='签到码', null=True, blank=True)
    checkin_qr = NullableImageField(verbose_name='签到二维码', editable=False)

    should_phase = models.ManyToManyField(Phase, verbose_name='参与成员', blank=True)

    class Meta:
        unique_together = ('name', 'date')
        ordering = ('-date', 'name')
        verbose_name = '会议和活动'
        verbose_name_plural = verbose_name
    objects = ActivityManager()

    def get_branches(self):
        return ','.join([str(b) for b in self.branch.all()])

    get_branches.short_description = '主办单位/党支部'

    def __str__(self):
        return "%s(%d-%02d-%02d)" % (self.name, self.date.year, self.date.month, self.date.day)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id is not None and self.checkin_code is not None:
            self.checkin_qr = generate_qrcode(self.id, self.checkin_code)
        super().save(force_insert, force_update, using, update_fields)


class TakeBaseManager(models.Manager):

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs).exclude(activity__date__lt=get_activity_start_date())


class TakeBase(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='学号')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动主题')

    class Meta:
        unique_together = ('activity', 'member')
        ordering = ('member', '-activity')
        abstract = True
    objects = TakeBaseManager()

    def get_member_branch(self):
        return self.member.branch

    def get_member_name(self):
        return self.member.name

    def get_member_netid(self):
        return self.member.netid

    def get_activity_type(self):
        return self.activity.atv_type

    def get_activity_date(self):
        return self.activity.date

    get_member_branch.short_description = '党支部'
    get_member_netid.short_description = '学号'
    get_member_name.short_description = '姓名'
    get_activity_date.short_description = '活动时间'
    get_activity_type.short_description = '活动类型'

    def __str__(self):
        return "%s: %s" % (self.activity, self.member)


class TakePartInBase(TakeBase):
    credit = models.FloatField('学时数', null=True, default=0)

    class Meta(TakeBase.Meta):
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.credit < 0.001 or self.activity.is_cascade and self.credit != self.activity.credit:
            self.credit = round(self.activity.credit, 2)
        super().save(force_insert, force_update, using, update_fields)


class TakePartIn(TakePartInBase):
    class Meta(TakePartInBase.Meta):
        verbose_name = '党员学时统计'
        verbose_name_plural = verbose_name


class TakePartIn2(TakePartInBase):
    class Meta(TakePartInBase.Meta):
        verbose_name = '非党员学时统计'
        verbose_name_plural = verbose_name


class Sharing(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='支部成员')
    when = models.DateTimeField('时间', default=timezone.now)
    title = models.CharField('标题', max_length=100, null=True)
    impression = models.TextField('学习心得', default='')
    impression_digest = models.CharField(max_length=255, null=True, editable=False)
    added = models.BooleanField('审核通过', default=False)

    class Meta:
        ordering = ('-when',)
        unique_together = ('member', 'title')
        verbose_name = '学习打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.member, self.title)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.impression:
            self.impression_digest = md5(self.impression)
        super(Sharing, self).save(force_insert, force_update, using, update_fields)


# 防止代签的表
class CheckIn(models.Model):
    activity_id = models.IntegerField()
    netid = models.IntegerField()
    ip = models.CharField(max_length=50)

    class Meta:
        unique_together = ('activity_id', 'netid')


# 请假、缺席统计表
class AskForLeave(TakeBase):
    status = models.SmallIntegerField('状态', choices=[
        (0, '缺席'), (1, '请假')
    ], default=0)

    class Meta(TakeBase.Meta):
        verbose_name = '请假、缺席统计'
        verbose_name_plural = verbose_name
