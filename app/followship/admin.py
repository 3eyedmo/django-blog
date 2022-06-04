from django.contrib import admin
from .models import FollowRequests

class FolloshipAdmin(admin.ModelAdmin):
    list_display=[
        "from_user",
        "to_user",
        "created",
        "status",
        "accepted_datetime"
    ]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.base_fields["accepted_datetime"].required = False
        return form

admin.site.register(FollowRequests, FolloshipAdmin)