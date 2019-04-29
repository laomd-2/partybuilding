from django.db import models

# Create your models here.
from django.utils.encoding import smart_str

from DjangoUeditor.models import UEditorField
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
    file = models.FileField('文件', upload_to=upload_to, null=True, blank=True)

    class Meta(NoteBase.Meta):
        verbose_name = '工作笔记'
        verbose_name_plural = verbose_name


class Rule(NoteBase):
    file = models.FileField('文件', upload_to=upload_to)

    class Meta(NoteBase.Meta):
        verbose_name = '规章制度'
        verbose_name_plural = verbose_name
