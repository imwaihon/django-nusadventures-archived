from django.contrib import admin
from party.models import Party, PartyInvite, PartyPost, PartyUser

# Register your models here.
admin.site.register(Party)
admin.site.register(PartyInvite)
admin.site.register(PartyPost)
admin.site.register(PartyUser)