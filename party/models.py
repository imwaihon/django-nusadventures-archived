from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.contrib import admin

from django import forms

from game.models import UserCharacter, Achievement, UserAchievement, UserCharacterForm, AchievementForm, UserAchievementForm

import hashlib

# Create your models here.
class Party(models.Model):
    name = models.CharField(max_length=300)
    creator = models.ForeignKey(User)
    description = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class PartyUser(models.Model):
	user = models.ForeignKey(User)
	party = models.ForeignKey(Party)

	def __unicode__(self):
		return self.user.get_username() + " " + self.party.name

class PartyInvite(models.Model):
	invited = models.ForeignKey(User)
	party = models.ForeignKey(Party)


	def __unicode__(self):
		return self.invited.get_username() + " " + self.party.name + "invite"

class PartyPost(models.Model):
	party = models.ForeignKey(Party)
	poster = models.ForeignKey(User)
	posttime = models.DateTimeField(auto_now_add=True)
	body = models.TextField(max_length=3000)

	def __unicode__(self):
		return self.party.name + " " + self.poster.get_username()


class PartyForm(forms.ModelForm):
    name = forms.CharField(max_length=300, help_text="Please enter a name for the party.")
    description = forms.CharField(widget=forms.Textarea, max_length=3000, help_text="Party Description")
    class Meta:
        # Provide an association between the ModelForm and a model

        model = Party
        exclude = ('creator',)

class PartyPostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, max_length=3000, help_text="Please enter your post.")

    class Meta:
        # Provide an association between the ModelForm and a model

        model = PartyPost
        exclude = ('party','poster')

class PartyInviteForm(forms.Form):
	username = forms.CharField(max_length=300, help_text="Please enter a username to invite.")

