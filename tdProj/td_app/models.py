from django.db import models
from django.contrib.auth.models import (AbstractUser)
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


# Inheriting from 'AbstractUser' lets us use all the fields of the default User,
# and overwrite the fields we need to change
# This is different from 'AbstractBaseUser', which only gets the password management features from the default User,
# and needs the developer to define other relevant fields.

class AppUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    # notice the absence of a "Password field", that is built in.

    # django uses the 'username' to identify users by default, but many modern applications use 'email' instead
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    
class Task(models.Model):
    content = models.CharField(max_length=100)
    priority = models.CharField(max_length = 1, validators =[RegexValidator(regex=r"[12345]")])
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
