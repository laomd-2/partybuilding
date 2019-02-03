from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Member
# Register your models here.


class MemberResource(resources.ModelResource):
    #
    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     super().before_import(dataset, using_transactions, dry_run, **kwargs)
    #     if dataset.headers:
    #         verbose2name = dict()
    #         fields = self._meta.model._meta.fields
    #         for f in fields:
    #             verbose2name[f.verbose_name] = f.name
    #         dataset.headers = [verbose2name[verbose] for verbose in dataset.headers]
    #         print(dataset.headers)

    class Meta:
        model = Member
        skip_unchanged = True   # 导入数据时，如果该条数据未修改过，则会忽略（默认根据id去匹配数据，可通过定义import_id_fields去更改）
        import_id_fields = ['学号']


class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource


admin.site.register(Member, MemberAdmin)
