from django.contrib import messages
from tablib import Dataset

from common import resources
from common.base import wrap
from common.rules import is_school_admin
from info.util import check_fields
from .models import Member, Branch


class MemberResource(resources.MyResource):
    excel_template = 'Excel模板/成员信息.xlsx'
    import_excel = excel_template

    class Meta:
        model = Member
        skip_unchanged = True
        import_id_fields = ('netid', )
        exclude = ['phase']

    def import_data(self, dataset: Dataset, dry_run=False, raise_errors=False,
                    use_transactions=None, collect_failed_rows=False, **kwargs):
        dataset.headers = dataset[2]
        for i in range(len(dataset.headers)):
            h = dataset.headers[i]
            if h is not None and '（' in h:
                h = h[: h.find('（')].strip()
                dataset.headers[i] = h
        dataset.lpop()
        dataset.lpop()
        dataset.lpop()
        return super().import_data(dataset, dry_run, raise_errors, use_transactions, collect_failed_rows, **kwargs)

    def before_import(self, dataset: Dataset, using_transactions, dry_run, **kwargs):
        super(MemberResource, self).before_import(dataset, using_transactions, dry_run, **kwargs)
        request = kwargs['request']
        m = request.user.member
        school_ad = is_school_admin(request.user)
        header = dataset.headers
        bi = header.index('branch')
        try:
            j = header.index('phone_number')
        except ValueError:
            j = -1

        _data = []
        for row in dataset:
            row = list(row)
            row[bi] = Branch.objects.get(branch_name=row[bi]).id
            if j >= 0 and row[j]:
                row[j] = '+86' + str(row[j])
            data = dict(zip(header, row))
            self.before_import_row(data)
            new_obj = Member()
            super(MemberResource, self).import_obj(new_obj, data, dry_run)
            if school_ad or (m is not None and new_obj.branch_id == m['branch_id']):
                error = []
                if check_fields(new_obj, error):
                    _data.append(tuple(row))
                else:
                    for e in error:
                        messages.warning(request, e)
            else:
                messages.warning(request, '您无权限修改/添加%s的成员%s。' % (str(new_obj.branch), str(new_obj)))
        dataset._data = _data

    def export_resource(self, obj):
        res = []
        for field in self.get_export_fields():
            value = getattr(obj, field.column_name)
            res.append(wrap(value))
        return res
