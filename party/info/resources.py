from django.db.models import F

from common import resources
from .models import Member, Branch


class MemberResource(resources.MyResource):
    class Meta:
        model = Member
        skip_unchanged = True
        import_id_fields = ('netid', )
        exclude = ('autobiography', 'application_form')

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        header = dataset.headers
        bi = header.index('党支部')
        try:
            j = header.index('联系电话')
        except ValueError:
            j = -1
        for i in range(len(dataset)):
            row = list(dataset[i])
            row[bi] = Branch.objects.get(branch_name=row[bi]).id
            if j >= 0:
                row[j] = '+86' + str(row[j])
            dataset[i] = tuple(row)
        super(MemberResource, self).before_import(dataset, using_transactions, dry_run, **kwargs)
