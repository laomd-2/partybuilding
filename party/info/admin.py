from django.contrib import admin
from .models import School, Branch, Member, Dependency


admin.site.register(School)
admin.site.register(Branch)
admin.site.register(Member)
admin.site.register(Dependency)
