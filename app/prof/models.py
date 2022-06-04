from django.db import models
from django.conf import settings

from datetime import datetime

def prof_image_dest(instance, filename):
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    destination = (
        f'profile/{year}-{month}-{day}/{instance.id}-{filename}'
    )
    return destination

class Profile(models.Model):
    class PrivacyChoices(models.TextChoices):
        PRIVATE = "PR"
        PUBLIC = "PU"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE
    )
    username = models.CharField(max_length=255 , null=True, unique=True, verbose_name="username")
    fullname = models.CharField(max_length=255, null=True)
    bio = models.CharField(max_length=2047, null=True)
    privacy = models.CharField(max_length=5, choices=PrivacyChoices.choices, default=PrivacyChoices.PUBLIC)
    image = models.ImageField(null = True, upload_to=prof_image_dest)
