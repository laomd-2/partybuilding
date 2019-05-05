from django.conf import settings
from django.db import models
# Create your models here.
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe

from DjangoUeditor.models import UEditorField
from common.storage import OverwriteStorage
from info.models import Branch


def upload_to(instance, filename):
    return type(instance)._meta.verbose_name + '/' + instance.branch.branch_name + '/' + smart_str(filename)


class NoteBase(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    author = models.CharField(verbose_name='作者', max_length=50, editable=False)
    branch = models.ForeignKey(Branch, verbose_name='党支部', on_delete=models.CASCADE, editable=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, editable=False)
    last_edit_time = models.DateTimeField(verbose_name='最后编辑时间', auto_now=True, editable=False)

    class Meta:
        ordering = ('-last_edit_time', 'author', 'create_time', 'title')
        unique_together = ('title', 'author')
        abstract = True

    def __str__(self):
        return "%s(%s)" % (self.title, self.author)


class Note(NoteBase):
    content = UEditorField(verbose_name='内容', toolbars='full', default='',
                           imagePath='note/images/', filePath='note/files/',
                           width='100%')
    file = models.FileField('文件', upload_to=upload_to, null=True, blank=True, storage=OverwriteStorage())

    class Meta(NoteBase.Meta):
        verbose_name = '工作笔记'
        verbose_name_plural = verbose_name


class Rule(NoteBase):
    file = models.FileField('文件', upload_to=upload_to, storage=OverwriteStorage())

    class Meta(NoteBase.Meta):
        verbose_name = '规章制度'
        verbose_name_plural = verbose_name


def upload_to2(instance, filename):
    return type(instance)._meta.verbose_name + '/' + instance.name + '/' + smart_str(filename)


class Files(models.Model):
    phases = ['入党积极分子', '重点发展对象', '预备党员', '正式党员', '首次组织谈话']
    name = models.CharField('阶段', max_length=50, choices=[(a, a) for a in phases], unique=True)
    notice = models.FileField(upload_to=upload_to2, verbose_name='通知', storage=OverwriteStorage(),
                              help_text='发送邮件时，这份材料在附件中。')
    files = models.FileField(upload_to=upload_to2, verbose_name='相关材料', null=True, blank=True,
                             storage=OverwriteStorage(), help_text='发送邮件时，这份材料在正文的链接中。')

    def __str__(self):
        return self.name

    def get_notice(self):
        return mark_safe(
            '<a href="%s/%s">%s</a>' % (settings.MEDIA_URL, self.notice.name, self.notice.name.split('/')[-1]))

    get_notice.short_description = '通知'

    def get_files(self):
        return mark_safe(
            '<a href="%s/%s">%s</a>' % (settings.MEDIA_URL, self.files.name, self.files.name.split('/')[-1]))

    get_files.short_description = '相关材料'

    class Meta:
        ordering = ('name',)
        verbose_name = '材料'
        verbose_name_plural = verbose_name
