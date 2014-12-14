from django.contrib import admin
from challenges.models import Challenge, UserChallenge, ChallengeTask, UserChallengeTask

# Register your models here.
admin.site.register(Challenge)
admin.site.register(UserChallenge)
admin.site.register(ChallengeTask)
admin.site.register(UserChallengeTask)
