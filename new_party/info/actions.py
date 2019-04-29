from datetime import datetime


def add_activist(modeladmin, request, queryset):
    queryset.filter(activist_date__isnull=True).update(activist_date=datetime.now())


def add_key_person(modeladmin, request, queryset):
    queryset.filter(key_develop_person_date__isnull=True) \
        .update(key_develop_person_date=datetime.now())


def add_premember(modeladmin, request, queryset):
    queryset.filter(first_branch_conference__isnull=True) \
        .update(first_branch_conference=datetime.now())


def add_fullmember(modeladmin, request, queryset):
    queryset.filter(second_branch_conference__isnull=True) \
        .update(second_branch_conference=datetime.now())


def merge_branch(modeladmin, request, queryset):
    t_branch = None
    target = None
    cur = -1
    # 迁移的目标支部默认是人数最多的
    for b in queryset:
        num_members = b.member_set.all().count()
        if target is None or num_members > cur:
            target = b.id
            t_branch = b
            cur = num_members
    queryset = queryset.exclude(id=target)
    for branch in queryset:
        # 将旧支部的所有东西迁移到新支部
        branch.member_set.update(branch_id=target)
        branch.oldmember_set.update(branch_id=target)
        branch.note_set.update(branch_id=target)
        branch.rule_set.update(branch_id=target)
        for atv in branch.activity_set.all():
            atv.branch.remove(branch)
            atv.branch.add(t_branch)
            atv.save()
    queryset.delete()


add_activist.short_description = '确定为入党积极分子'
add_key_person.short_description = '确定为重点发展对象'
add_premember.short_description = '确定为预备党员'
add_fullmember.short_description = '确定为正式党员'
merge_branch.short_description = '合并 所选的党支部'
