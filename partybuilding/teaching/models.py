from django.db import models
from info.models import Member


class Credit(models.Model):
    activity = models.CharField('活动主题', max_length=100)
    date = models.DateField('活动时间', max_length=10)
    netid = models.OneToOneField(Member, on_delete=models.CASCADE, verbose_name='活动人员')
    credit = models.FloatField('学时数', choices=[(i / 2, i / 2) for i in range(1, 41)])

    class Meta:
        unique_together = ('activity', 'date', 'netid')
        ordering = ('-date', 'activity', 'netid')
        verbose_name = '学时统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s: %s %s" % (self.date, self.activity, self.netid, self.credit)
