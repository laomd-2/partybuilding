from django.contrib import messages
from tablib import Dataset

from common import resources
from common.base import wrap
from common.rules import is_school_admin
from info.util import check_fields
from .models import Member, Branch


class MemberResource(resources.MyResource):
    excel_template = 'Excel模板/成员信息.xlsx'

    class Meta:
        model = Member
        skip_unchanged = True
        import_id_fields = ('netid', )

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
                if check_fields(request, new_obj, msg=messages.warning):
                    _data.append(tuple(row))
            else:
                messages.warning(request, '您无权限修改/添加%s的成员%s。' % (str(new_obj.branch), str(new_obj)))
        dataset._data = _data

    def export_resource(self, obj):
        res = []
        for field in self.get_export_fields():
            value = getattr(obj, field.column_name)
            res.append(wrap(value))
        return res
