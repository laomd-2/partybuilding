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
            dataset[i] = tuple(row)
        super(MemberResource, self).before_import(dataset, using_transactions, dry_run, **kwargs)

    # def before_import_row(self, row, **kwargs):
    #     row['branch'] = Branch.objects.get(branch_name=row['branch']).id
    #     super(MemberResource, self).before_import_row(row, **kwargs)
