from django.contrib import admin

from .models import UserProfile, MovieWatch

admin.site.register(UserProfile)
admin.site.register(MovieWatch)
