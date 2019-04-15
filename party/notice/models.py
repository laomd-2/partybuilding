import datetime

from django.db import models

from info.models import NullableDateField, Branch


class FirstTalk(models.Model):
    branch = models.ForeignKey(Branch, verbose_name='党支部', on_delete=models.CASCADE)
    netid = models.IntegerField('学号', primary_key=True)
    name = models.CharField('姓名', max_length=20)
    application_date = NullableDateField(verbose_name='递交入党申请书时间')

    class Meta:
        verbose_name = '首次组织谈话'
        verbose_name_plural = verbose_name
        ordering = ('branch', 'netid')

    def talk_date_end(self):
        return self.application_date + datetime.timedelta(days=30)

    talk_date_end.short_description = '谈话截止时间'


class Activist(models.Model):
    branch = models.ForeignKey(Branch, verbose_name='党支部', on_delete=models.CASCADE)
    netid = models.IntegerField('学号', primary_key=True)
    name = models.CharField('姓名', max_length=20)
    application_date = models.DateField(verbose_name='递交入党申请书时间')

    class Meta:
        verbose_name = '%d月可接收积极分子' % datetime.datetime.now().month
        verbose_name_plural = verbose_name
        ordering = ('branch', 'netid')


class KeyDevelop(models.Model):
    branch = models.ForeignKey(Branch, verbose_name='党支部', on_delete=models.CASCADE)
    netid = models.IntegerField('学号', primary_key=True)
    name = models.CharField('姓名', max_length=20)
    activist_date = models.DateField(verbose_name='确定为入党积极分子时间')

    class Meta:
        verbose_name = '%d月可接收发展对象' % datetime.datetime.now().month
        verbose_name_plural = verbose_name
        ordering = ('branch', 'netid')


class PreMember(models.Model):
    branch = models.ForeignKey(Branch, verbose_name='党支部', on_delete=models.CASCADE)
    netid = models.IntegerField('学号', primary_key=True)
    name = models.CharField('姓名', max_length=20)
    key_develop_person_date = models.DateField(verbose_name='确定为重点发展对象时间')

    class Meta:
        verbose_name = '%d月预备党员预审' % datetime.datetime.now().month
        verbose_name_plural = verbose_name
        ordering = ('branch', 'netid')


class FullMember(models.Model):
    branch = models.ForeignKey(Branch, verbose_name='党支部', on_delete=models.CASCADE)
    netid = models.IntegerField('学号', primary_key=True)
    name = models.CharField('姓名', max_length=20)
    application_date = models.DateField(verbose_name='递交入党申请书时间')
    first_branch_conference = models.DateField(verbose_name='确定为预备党员时间')
    application_fullmember_date = models.DateField(verbose_name='递交转正申请书时间')

    class Meta:
        verbose_name = '%d月可转正预备党员' % datetime.datetime.now().month
        verbose_name_plural = verbose_name
        ordering = ('branch', 'netid')
