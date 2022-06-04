from datetime import datetime


from django.db import models
from django.conf import settings


def post_img_destination(instance, filename):
    post_id = instance.author.id
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    destination = (
        f"posts/{year}-{month}-{day}/{post_id}/{filename}"
    )
    return destination


class Post(models.Model):
    image = models.ImageField(upload_to = post_img_destination)
    body = models.CharField(max_length=5000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name= "posts",
        on_delete= models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        through="LikeAction"
    )

    def __str__(self):
        return self.author.email + " created post with id :  " + str(self.id)

class LikeAction(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="like_action",
        on_delete=models.SET_NULL,
        null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="like_action",
        on_delete=models.SET_NULL,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            "user",
            "post"
        ]





class Comment(models.Model):
    text = models.CharField(max_length=1023)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.SET_NULL,
        null=True
    )
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.SET_NULL,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


