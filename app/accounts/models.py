import uuid

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken

from followship.models import FollowRequests
from prof.models import Profile


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_blog_user(self, email, password):
        if not email:
            raise ValueError('you must have atleast email or phone number')
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name=_('user email address'),
        max_length=255,
        unique=True,
    )
    followings = models.ManyToManyField(
        "self",
        related_name="followers",
        through= FollowRequests,
        symmetrical=False
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_following(self, to_user):
        query = FollowRequests.objects.filter(from_user=self, to_user=to_user).exists()
        if query:
            return True
        return False

    def has_follower(self, from_user):
        query = FollowRequests.objects.filter(from_user=from_user, to_user=self).exists()
        if query:
            return True
        return False

    def get_followers(self, only_list=[], pending=False):
        if pending:
            followers = self.followers.filter(following_req__status = "P")
        else:
            followers = self.followers.filter(following_req__status = "A")
        if len(only_list):
            followers = followers.only(*only_list)
        return followers

    def get_followings(self, only_list=[], pending=False):
        if pending:
            followings = self.followings.filter(follow_req__status="A")
        else:
            followings = self.followings.filter(follow_req__status="A")
        if len(only_list):
            followings = followings.only(*only_list)
        
        return followings

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    def is_staff_user(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_staff
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        tokens = {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }
        return tokens

    @property
    def is_superuser(self):
        return self.is_admin




def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user = instance)
        profile.save()


post_save.connect(create_profile, sender=MyUser)