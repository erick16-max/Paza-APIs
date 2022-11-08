from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError()
        if not username:
            raise ValueError()

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.admin = True
        user.staff = True
        user.superuser = True
        user.save()
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=12, primary_key=True, unique=True)
    id = models.IntegerField(default=1)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    association = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser
    @property
    def is_active(self):
        return self.active