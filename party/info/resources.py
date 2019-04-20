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
        for i in range(len(dataset)):
            row = list(dataset[i])
            row[0] = Branch.objects.get(branch_name=row[0]).id
            try:
                if row[7]:
                    row[7] = '+86' + str(row[7])
            except IndexError:
                pass
            dataset[i] = tuple(row)
        super(MemberResource, self).before_import(dataset, using_transactions, dry_run, **kwargs)
