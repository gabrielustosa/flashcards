from django.contrib import admin

from flashcards.apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
