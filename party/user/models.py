from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from user.util import get_bind_member
from info.models import *
from .base_user import AbstractBaseUser


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    email = models.EmailField(_('邮箱'), blank=True)
    is_staff = models.BooleanField(
        '允许登录',
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractBaseUser.Meta):
        verbose_name = '我的账号'
        verbose_name_plural = verbose_name
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ('-last_login', 'username')

    @cached_property
    def member(self):
        return get_bind_member(self)

    @cached_property
    def school(self):
        return School.objects.filter(id=int(self.username[0])).values('id', 'name')[0]

    @property
    def school_id(self):
        return self.username[0]

    def get_member(self):
        m = self.member
        if m is not None:
            return m['name']
        else:
            return ''
    get_member.short_description = '姓名'
