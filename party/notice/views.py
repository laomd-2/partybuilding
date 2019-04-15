from django.shortcuts import render

# Create your views here.
from common.rules import *
from user.util import get_bind_member


def queryset(request, model):
    if is_member(request.user):
        m = get_bind_member(request.user)
        if m is not None:
            return model.objects.filter(netid=m.netid)
    elif is_branch_manager(request.user):
        m = get_bind_member(request.user)
        if m is not None:
            return model.objects.filter(branch=m.branch)
    elif is_school_manager(request.user):
        school = int(request.user.username[0])
        return model.objects.filter(branch__school_id=school)
    elif request.user.is_superuser:
        return model.objects.all()
    return model.objects.none()
