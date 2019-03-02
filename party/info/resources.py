from common import resources
from .models import Member


class MemberResource(resources.MyResource):
    class Meta:
        model = Member
        skip_unchanged = True
        import_id_fields = ('netid', )

