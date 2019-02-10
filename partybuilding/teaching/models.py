from django.db import models
from django.utils import timezone
from info.models import Member, Branch


class Activity(models.Model):
    name = models.CharField('活动名称', max_length=100)
    date = models.DateTimeField('活动时间', default=timezone.now)
    credit = models.FloatField('学时数', choices=((i / 2, i / 2) for i in range(1, 41)))
    visualable_others = models.BooleanField('其他支部可见', default=False)
    branch = models.ManyToManyField(Branch, verbose_name='主/承办党支部')

    class Meta:
        unique_together = ('name', 'date')
        ordering = ('-date', 'name')
        verbose_name = '党建活动'
        verbose_name_plural = verbose_name

    def get_branches(self):
        return ','.join([str(b) for b in self.branch.all()])

    get_branches.short_description = '主/承办党支部'

    def __str__(self):
        return "%s%s" % (self.name, ("(" + str(self.id) + ")") if self.id else '')


class TakePartIn(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='支部成员学号')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='党建活动ID')
    date = models.DateTimeField('活动时间', null=True)
    credit = models.FloatField('学时数', null=True)

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
