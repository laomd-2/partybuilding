from common import resources
from .models import Activity, TakePartIn
from info.models import Member


class ActivityResource(resources.MyResource):
    class Meta:
        model = Activity
        skip_unchanged = True
        import_id_fields = ('name', 'date')
        exclude = ('id', 'cascade', 'branch', 'visualable_others')


class CreditResource(resources.MyResource):
    class Meta:
        model = TakePartIn
        skip_unchanged = True
        import_id_fields = ('member', 'activity')
        exclude = ('id', 'last_modified')

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for i in range(len(dataset)):
            row = list(dataset[i])
            row[0] = Member.objects.get(name=row[0]).pk
            dataset[i] = tuple(row)
        super(CreditResource, self).before_import(dataset, using_transactions, dry_run, **kwargs)
