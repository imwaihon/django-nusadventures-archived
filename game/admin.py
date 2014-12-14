from django.contrib import admin
from game.models import UserCharacter, UserAchievement, Achievement
# Register your models here.
admin.site.register(UserCharacter)
admin.site.register(Achievement)
admin.site.register(UserAchievement)