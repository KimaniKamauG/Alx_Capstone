from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Email is very much required.')
        if not password:
            raise ValueError('Password ought to be provided!')
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)
        return user 
    
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=20)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']





# class UserProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
#     email = models.EmailField(max_length=255)
#     image = models.ImageField(default='default.jpg', upload_to='profile_pictures', blank=True, null=True)

#     def __str__(self):
#         return f'{self.user.username} Profile'
    
# @receiver(post_save, sender=CustomUser)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         user_profile = UserProfile.objects.create(user=instance)
#         user_profile.save()  