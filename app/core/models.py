"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# users can have no password (for test cases. user won't be able to login)
class UserManager(BaseUserManager):
    """Manager for users
       https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    """
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user
        """
        if not email:
            raise ValueError('User must have an email address')
        # The same as defining a new user with User class
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # Hash password
        user.set_password(password)
        # `using` is to support multiple databases (if this is the case in the project)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_stuff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'