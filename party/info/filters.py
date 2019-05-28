from django.contrib.admin import SimpleListFilter


class PhaseFilter(SimpleListFilter):
    title = '阶段'
    parameter_name = 'phase'

    def lookups(self, request, model_admin):
        return (
            (0, '正式党员'),
            (1, '预备党员'),
            (2, '发展对象'),
            (3, '积极分子'),
            (4, '提交入党申请书')
        )

    def queryset(self, request, queryset):
        v = self.value()
        if v == 0:
            return queryset.filter(second_branch_conference__isnull=False)
        elif v == 1:
            return queryset.filter(second_branch_conference__isnull=True,
                                   first_branch_conference__isnull=False)
        elif v == 2:
            return queryset.filter(first_branch_conference__isnull=True,
                                   key_develop_person_date__isnull=False)
        elif v == 3:
            return queryset.filter(key_develop_person_date__isnull=True,
                                   activist_date__isnull=False)
        elif v == 4:
            return queryset.filter(activist_date__isnull=True,
                                   application_date__isnull=False)
        return queryset
