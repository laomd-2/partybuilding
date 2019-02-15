from common import resources
from .models import Activity, TakePartIn


# class ActivityResource(resources.ModelResource):
#     class Meta:
#         model = Activity
#         skip_unchanged = True
#         import_id_fields = ('name', 'branch', 'date')
#

class CreditResource(resources.MyResource):
    class Meta:
        model = TakePartIn
        skip_unchanged = True
        import_id_fields = ('member', 'activity')
