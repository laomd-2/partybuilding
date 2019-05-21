from info.models import Member


def get_bind_member(user):
    try:
        return Member.objects.filter(netid=int(user.username)).values('netid', 'name', 'branch_id')[0]
    except Member.DoesNotExist:
        return None
    except IndexError:
        return None
