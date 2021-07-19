from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib import auth
# from django.contrib.auth.models import Group


class UserManager(BaseUserManager):
    """
    Custom user model manager, with email as unique identifier.
    """

    def create_user(
        self,
        email,
        username,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserModel(AbstractUser):
    user_type_choices = [('Customers', 'Customer'),
                         ('Farmers', 'Farmer')]
    username = models.CharField(
        verbose_name='Username',
        max_length=20,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    date_joined = models.DateTimeField(
        verbose_name='date joined',
        default=timezone.now,
    )
    user_type = models.CharField(
        verbose_name='User type',
        max_length=20,
        choices=user_type_choices,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
