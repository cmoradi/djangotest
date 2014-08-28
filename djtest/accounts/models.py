from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import BaseUserManager

from django.conf import settings


class PortalUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class PortalUser(AbstractBaseUser, PermissionsMixin):
    # Wagtail requires the username to be defined.
    slate_id = models.CharField('slate ID', max_length=9,
                                unique=True, db_index=True)
    
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    email = models.EmailField(_('email address'), max_length=255, unique=True,)
    slate_guid = models.CharField('slate GUID', max_length=44,
                                unique=True, db_index=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active.  Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = PortalUserManager()

    USERNAME_FIELD = 'slate_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

