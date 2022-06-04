from typing import Any

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class FollowRequests(models.Model):
    class FollowshipStatus(models.TextChoices):
        PENDING = 'P'
        ACCEPTED = 'A'

    is_cleaned = False

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="following_req",
        on_delete = models.SET_NULL,
        null= True
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="follow_req",
        on_delete=models.SET_NULL,
        null=True
    )
    status = models.CharField(
        max_length=255,
        choices=FollowshipStatus.choices,
        default=FollowshipStatus.PENDING
    )
    created = models.DateTimeField(auto_now_add=True)
    accepted_datetime = models.DateTimeField(null=True)


    class Meta:
        unique_together = [
            "from_user",
            "to_user"
        ]

    def clean(self) -> None:
        self.is_cleaned = True
        from_user = self.from_user
        to_user = self.to_user
        if from_user and to_user:
            if from_user == to_user:
                raise ValidationError("from_user and to_user are same")
            super().clean()
            return True
        raise ValidationError("credintial is not satisfied.")

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()

        super().save(*args, **kwargs)

