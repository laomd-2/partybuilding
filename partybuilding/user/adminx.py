import xadmin
from .models import User


class UserAdmin(object):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username']
    list_editable = ['username', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['username']


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
