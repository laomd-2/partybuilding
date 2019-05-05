import rules
import datetime
from django.contrib.auth.models import Group

# 三个cache
identity = [dict(), dict(), dict()]


def cached_wrapper(group):
    def _inner(func):
        def inner(user):
            now = datetime.datetime.now()
            last = identity[group].get(user.username, (0, False))
            if last[0] == 0 or (now - last[0]).seconds > 3:
                last = identity[group][user.username] = (now, bool(func(user)))
            return last[1]

        return inner

    return _inner


@rules.predicate
@cached_wrapper(group=0)
def is_branch_manager(user):
    return user.groups.filter(name='党支部管理员').exists()


@rules.predicate
@cached_wrapper(group=1)
def is_school_manager(user):
    return user.groups.filter(name='党辅').exists()


@rules.predicate
@cached_wrapper(group=2)
def is_member(user):
    return user.groups.filter(name='普通成员').exists()


is_school_admin = is_school_manager | rules.is_superuser
is_branch_admin = is_branch_manager | rules.is_superuser
is_admin = is_branch_admin | is_school_admin
