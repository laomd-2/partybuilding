import datetime
from info.models import Member, Dependency


def verbose_name(fields):
    res = []
    for field in fields:
        try:
            res.append(Member._meta.get_field(field).verbose_name)
        except:
            res.append(getattr(Member, field).short_description)
    return res


def get_ym(m1, m2):
    if m1 > m2:
        m1, m2 = m2, m1
    today = datetime.datetime.today()
    if today.month <= m2:
        year = today.year
        if today.month <= m1:
            month = m1
        else:
            month = m2
    else:
        year = today.year + 1
        month = m1
    return year, month


class FirstTalk:
    fields = ['branch', 'netid', 'name', 'application_date', 'first_talk_end']
    verbose_name = '首次组织谈话'

    @staticmethod
    def filter(**kwargs):
        end = datetime.datetime.today() - datetime.timedelta(days=30)
        return Member.objects.filter(**kwargs, activist_date__isnull=True,
                                     application_date__isnull=False,
                                     application_date__gte=end)


class Activist:
    fields = ['branch', 'netid', 'name', 'application_date']
    verbose_name = '%d年%d月可接收入党积极分子' % get_ym(3, 9)

    @staticmethod
    def filter(**kwargs):
        year, month = get_ym(3, 9)
        end = datetime.date(year, month, 30)
        try:
            days = Dependency.objects.get(from_1='application_date', to='activist_date').days
            end = end - datetime.timedelta(days=days)
        except Dependency.DoesNotExist:
            pass
        return Member.objects.filter(**kwargs, activist_date__isnull=True,
                                     application_date__isnull=False,
                                     application_date__lt=end)


class KeyDevelop:
    fields = ['branch', 'netid', 'name', 'activist_date']
    verbose_name = '%d年%d月可接收重点发展对象' % get_ym(3, 9)

    @staticmethod
    def filter(**kwargs):
        print(kwargs.items())
        year, month = get_ym(3, 9)
        end = datetime.date(year, month, 30)
        try:
            days = Dependency.objects.get(from_1='activist_date', to='key_develop_person_date').days
            end = end - datetime.timedelta(days=days)
        except Dependency.DoesNotExist:
            pass
        return Member.objects.filter(**kwargs, key_develop_person_date__isnull=True,
                                     activist_date__isnull=False,
                                     activist_date__lt=end)


class PreMember:
    fields = ['branch', 'netid', 'name', 'key_develop_person_date']
    verbose_name = '%d年%d月可接收预备党员' % get_ym(6, 12)

    @staticmethod
    def filter(**kwargs):
        year, month = get_ym(6, 12)
        end = datetime.date(year, month, 30)
        try:
            days = Dependency.objects.get(from_1='key_develop_person_date', to='first_branch_conference').days
            end = end - datetime.timedelta(days=days)
        except Dependency.DoesNotExist:
            pass
        return Member.objects.filter(**kwargs, first_branch_conference__isnull=True,
                                     key_develop_person_date__isnull=False,
                                     key_develop_person_date__lt=end)


class FullMember:
    fields = ['branch', 'netid', 'name', 'application_date', 'first_branch_conference', 'application_fullmember_date']
    verbose_name = '%d年%d月可转正预备党员' % get_ym(6, 12)

    @staticmethod
    def filter(**kwargs):
        year, month = get_ym(6, 12)
        end = datetime.date(year, month, 30)
        try:
            days = Dependency.objects.get(from_1='first_branch_conference', to='second_branch_conference').days
            end = end - datetime.timedelta(days=days)
        except Dependency.DoesNotExist:
            pass
        return Member.objects.filter(**kwargs, second_branch_conference__isnull=True,
                                     first_branch_conference__isnull=False,
                                     first_branch_conference__lt=end)
