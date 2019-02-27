from django.db import models
from django.utils import timezone
from info.models import Member, Branch


class Activity(models.Model):
    name = models.CharField('主题', max_length=100)
    date = models.DateTimeField('开始时间', default=timezone.now)
    end_time = models.DateTimeField('结束时间', default=timezone.now)
    atv_type_choices = ['集中学习', '集中教育', '个人自学', '其他']
    atv_type = models.CharField('活动类型', choices=[
        (t, t) for t in atv_type_choices
    ], default='集中学习', max_length=10)
    credit = models.FloatField('学时数', default=0, choices=sorted([(0.1, 0.1), (0.2, 0.2)] + [
        (i / 2, i / 2) for i in range(41)
    ]))
    visualable_others = models.BooleanField('其他支部可见', default=False)
    branch = models.ManyToManyField(Branch, verbose_name='主/承办党支部')

    class Meta:
        unique_together = ('name', 'date')
        ordering = ('-date', 'name')
        verbose_name = '会议/活动'
        verbose_name_plural = verbose_name

    def get_branches(self):
        return ','.join([str(b) for b in self.branch.all()])
    get_branches.short_description = '主/承办党支部'

    def __str__(self):
        return "%s(%d/%02d/%02d)" % (self.name, self.date.year, self.date.month, self.date.day)


class TakePartIn(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='支部成员')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='会议/活动')
    # date = models.DateTimeField('开始时间', null=True)
    # end_time = models.DateTimeField('结束时间', null=True)
    credit = models.FloatField('学时数', null=True, default=0, choices=sorted([(0.1, 0.1), (0.2, 0.2)] + [
        (i / 2, i / 2) for i in range(41)
    ]))

    class Meta:
        unique_together = ('activity', 'member')
        ordering = ('activity', 'member')
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
        fields['支部成员ID'] = 'member'
        fields['会议/活动ID'] = 'activity'
        return fields

    @staticmethod
    def foreign_keys():
        return ['member', 'activity']
