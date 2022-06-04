from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = [
            "id",
            "body",
            "author",
            "image"
        ]
        extra_kwargs = {
            "image": {
                "required": False
            }
        }
        
