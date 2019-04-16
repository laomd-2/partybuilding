from django.utils.encoding import force_text

from common import resources
from .models import Activity, TakePartIn


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
