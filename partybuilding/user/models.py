from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class User(AbstractUser):
    username = models.CharField(_('学号'), max_length=8, primary_key=True)
    first_name = last_name = None

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    @property
    def id(self):
        return ""
