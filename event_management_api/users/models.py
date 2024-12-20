from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Email is very much required.')
        if not password:
            raise ValueError('Password ought to be provided!')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)
        return user 
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=False, max_length=20)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


        