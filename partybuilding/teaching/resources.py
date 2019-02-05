from import_export import resources
from .models import Credit


class CreditResource(resources.ModelResource):
    class Meta:
        model = Credit
        skip_unchanged = True
        import_id_fields = ('netid', 'activity')
