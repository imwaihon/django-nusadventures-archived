from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.contrib import admin

from django import forms

from game.models import UserCharacter, Achievement, UserAchievement, UserCharacterForm, AchievementForm, UserAchievementForm

import hashlib

# Create your models here.

class Challenge(models.Model):
    name = models.CharField(max_length=300)
    creator = models.ForeignKey(User)
    description = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name    

class UserChallenge(models.Model):
    challenge = models.ForeignKey(Challenge)
    user = models.ForeignKey(User)
    started = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)

    def __unicode__(self):
        return self.challenge.name  


class ChallengeTask(models.Model):
    name       = models.CharField(max_length=300)
    challenge  = models.ForeignKey(Challenge)
    body       = models.TextField(max_length=3000, default='', blank=True)
    priority   = models.IntegerField(default=0, blank=True, null=True)


    def __unicode__(self):
        return self.name

class UserChallengeTask(models.Model):
    challenge = models.ForeignKey(UserChallenge)
    challengetask  = models.ForeignKey(ChallengeTask)
    progress   = models.IntegerField(default=0)
    closed     = models.BooleanField(default=False)
    completed  = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.challengetask.name




class ChallengeForm(forms.ModelForm):
    name = forms.CharField(max_length=200, help_text="Please enter a name for the challenge.")
    description = forms.CharField(widget=forms.Textarea, max_length=3000,  help_text="Please enter a description.")


    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model

        model = Challenge
        exclude = ('creator',)


class ChallengeTaskForm(forms.ModelForm):
    name       = forms.CharField(max_length=300, help_text="Please enter a name for the task.")
    body       = forms.CharField(widget=forms.Textarea, max_length=3000, help_text="Task Description")
    priority   = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = ChallengeTask
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        fields = ('name', 'body', 'priority')


class UserChallengeForm(forms.ModelForm):


    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model

        model = UserChallenge
        exclude = ('challenge','user')


class UserChallengeTaskForm(forms.ModelForm):


    class Meta:
        # Provide an association between the ModelForm and a model
        model = UserChallengeTask
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.