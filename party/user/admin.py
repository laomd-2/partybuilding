from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        g = Group.objects.get(name='普通成员')
        if created:
            instance.groups.add(g)
    except:
        pass


# admin.site.unregister(User)
admin.site.register(User)
