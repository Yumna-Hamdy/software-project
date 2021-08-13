from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username,first_name ,last_name , age, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not age:
            raise ValueError('Users must have an age')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, first_name ,last_name , age):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_pro = True
        user.save(using=self._db)
        return user


AUTH_PROVIDERS = {'facebook': 'facebook',
                  'email': 'email'}
class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True, db_index=True)
    first_name = models.CharField(verbose_name='first-name', max_length=60)
    last_name = models.CharField(verbose_name='last-name', max_length=60)
    age = models.IntegerField( validators=[
            MaxValueValidator(110),
            MinValueValidator(0)
        ])
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app?
    def has_module_perms(self, app_label):
        return True

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
