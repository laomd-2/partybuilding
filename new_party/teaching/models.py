from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.encoding import smart_str

from info.models import Member, Branch
import datetime


def upload_to(instance, filename):
    return Activity._meta.verbose_name + '/' + str(instance) + '/' + smart_str(filename)


class NullableImageField(models.ImageField):

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        kwargs['upload_to'] = upload_to
        kwargs['null'] = kwargs['blank'] = True
        super().__init__(verbose_name, name, width_field, height_field, **kwargs)


class Activity(models.Model):
    name = models.CharField('活动名称', max_length=100)
    date = models.DateTimeField('开始时间', default=timezone.now)
    end_time = models.DateTimeField('结束时间', default=timezone.now)
    atv_type_choices = ['集中学习', '集中教育', '个人自学', '其他']
    atv_type = models.CharField('活动类型', choices=[
        (t, t) for t in atv_type_choices
    ], default='集中学习', max_length=10)
    branch = models.ManyToManyField(Branch, verbose_name='主/承办党支部')
    credit = models.FloatField('学时数', default=0)
    cascade = models.BooleanField('级联更新', default=False, help_text='当会议/活动的学时数改变时，自动在学时统计中更新。')
    visualable_others = models.BooleanField('公开', default=False, help_text='是否向其他支部公开。')
    image1 = NullableImageField(verbose_name='活动照片1')
    image2 = NullableImageField(verbose_name='活动照片2')
    image3 = NullableImageField(verbose_name='活动照片3')
    image4 = NullableImageField(verbose_name='活动照片4')
    image5 = NullableImageField(verbose_name='活动照片5')

    class Meta:
        unique_together = ('name', 'date')
        ordering = ('-date', 'name')
        verbose_name = '会议和活动'
        verbose_name_plural = verbose_name

    def get_branches(self):
        return ','.join([str(b) for b in self.branch.all()])
    get_branches.short_description = '主/承办党支部'

    def __str__(self):
        return "%s(%d-%02d-%02d)" % (self.name, self.date.year, self.date.month, self.date.day)

    @staticmethod
    def foreign_keys():
        return ['branch']


class TakePartIn(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='支部成员')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='会议/活动')
    credit = models.FloatField('学时数', null=True, default=0)
    last_modified = models.DateTimeField('最后修改时间', default=timezone.now)

    class Meta:
        unique_together = ('activity', 'member')
        ordering = ('-last_modified', '-credit', 'member')
        verbose_name = '学时统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s: %s" % (self.activity, self.member)

    @staticmethod
    def necessary_fields():
        return ['member', 'activity']

    @staticmethod
    def export_field_map():
        fields = dict()
        fields['支部成员'] = 'member'
        fields['会议/活动'] = 'activity'
        return fields

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            old = TakePartIn.objects.get(id=self.id)
            if self.activity.cascade and self.credit != self.activity.credit:
                return
            if old.activity != self.activity or abs(old.credit - self.credit) > 0.001:
                self.last_modified = datetime.datetime.now()
        except TakePartIn.DoesNotExist:
            self.credit = Activity.objects.get(id=self.activity_id).credit
        self.credit = round(self.credit, 1)
        super().save(force_insert, force_update, using, update_fields)


class Sharing(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='支部成员')
    when = models.DateTimeField('时间', default=timezone.now)
    title = models.CharField('标题', max_length=100, null=True)
    impression = models.TextField('学习心得', default='')
    added = models.BooleanField('审核通过', default=False)

    class Meta:
        ordering = ('-when', )
        verbose_name = '学习打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.member, self.title)

    @staticmethod
    def foreign_keys():
        return ['member']

    def validate_unique(self, exclude=None):
        if self.pk is None:
            if Sharing.objects.filter(member=self.member, title=self.title):
                raise ValidationError("%s已经学习过%s。" % (self.member, self.title))
