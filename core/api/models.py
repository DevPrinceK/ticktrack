from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    staff_id = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def get_fullname(self):
        '''return the full name of the user'''
        return self.fullname if self.fullname else self.staff_id if self.staff_id else 'Anonymous'  # noqa

    objects = AccountManager()

    USERNAME_FIELD = 'staff_id'

    def __str__(self):
        return self.get_fullname()

    class Meta:
        db_table = 'user'
