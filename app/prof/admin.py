from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'image',
        'user',
        'fullname',
        'bio'
    ]

admin.site.register(Profile, ProfileAdmin)