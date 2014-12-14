from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

# Create your models here.
class UserCharacter(models.Model):
	user = models.ForeignKey(User)
	level = models.IntegerField(default=1)
	totalExpAmt = models.IntegerField(default=0)
	expAmt = models.IntegerField(default=0)
	taskAmt = models.IntegerField(default=0)
	contribAmt = models.IntegerField(default=0)
	upvoteAmt = models.IntegerField(default=0)
	challengeAmt = models.IntegerField(default=0)
	description = models.TextField(max_length=3000, blank=True)

   	def __unicode__(self):
   		return self.user.username

   	def profile_image_url(self):
   		fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
   		if len(fb_uid):
   			return "http://graph.facebook.com/{}/picture?width=100&height=100".format(fb_uid[0].uid)


   	class Meta:
		unique_together = ["user"]


class Achievement(models.Model):
	name = models.CharField(max_length=256, unique=True)
	badge = models.ImageField(upload_to='badge_images', blank=True)
	description = models.TextField(max_length=3000)

	def __unicode__(self):
		return self.name

class UserAchievement(models.Model):
	user = models.ForeignKey(User)
	achievement = models.ForeignKey(Achievement)

	def __unicode__(self):
		return self.user.username + "-" + self.achievement.name


class UserCharacterForm(forms.ModelForm):
	level = forms.IntegerField(initial=1)
	expAmt = forms.IntegerField(initial=0)
	taskAmt = forms.IntegerField(initial=0)
	contribAmt = forms.IntegerField(initial=0)
	upvoteAmt = forms.IntegerField(initial=0)
	challengeAmt = forms.IntegerField(initial=0)

	class Meta:
		model = UserCharacter


class UserAchievementForm(forms.ModelForm):

	class Meta:
		model = UserAchievement



class AchievementForm(forms.ModelForm):
	name = forms.CharField(widget=forms.Textarea, max_length=256)
	badge = forms.ImageField(help_text="Select a profile image to upload.", required=False)
	description = forms.CharField(widget=forms.Textarea, max_length=3000)

	class Meta:
		model = Achievement



