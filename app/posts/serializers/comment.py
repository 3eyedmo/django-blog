from rest_framework import serializers
from posts.models import Comment


class CurrentPostDefault:
    requires_context = True
    def __call__(self, serializer_field):
        return serializer_field.context['post']

    def __repr__(self):
        return '%s()' % self.__class__.__name__

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.HiddenField(default=CurrentPostDefault())
    class Meta:
        model= Comment
        fields= [
            "id",
            "text",
            "user",
            "post"
        ]
