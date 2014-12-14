from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.contrib import admin

from django import forms

from game.models import UserCharacter, Achievement, UserAchievement, UserCharacterForm, AchievementForm, UserAchievementForm

import hashlib

# Create your models here.

class FixedModule(models.Model):
	code = models.CharField(max_length=60)
	name = models.TextField(max_length=200)
	description = models.TextField(max_length=3000)

   	def __unicode__(self):
   		return self.code
   	class Meta:
		unique_together = ["code"]


class Module(models.Model):
    completed = models.BooleanField(default=False)
    fixedModule = models.ForeignKey(FixedModule)
    creator = models.ForeignKey(User, blank=True, related_name="modules")

    def getCode(self):
		return self.fixedModule.code

    def getName(self):
		return self.fixedModule.name

    def __unicode__(self):
		return self.fixedModule.code
    class Meta:
		unique_together = ["creator","fixedModule"]

class Task(models.Model):
    name       = models.CharField(max_length=300)
    module     = models.ForeignKey(Module)
    creator    = models.ForeignKey(User, related_name="tasks")
    body       = models.TextField(max_length=3000, default='', blank=True)
    priority   = models.IntegerField(default=0, blank=True, null=True)
    progress   = models.IntegerField(default=0)
    closed     = models.BooleanField(default=False)
    created    = models.DateTimeField(auto_now_add=True)
    completed  = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name




class ModuleForm(forms.ModelForm):
    fixedModule = forms.ModelChoiceField(queryset=FixedModule.objects.all().order_by('code'))


    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model

        model = Module
        exclude = ('creator','completed')



class TaskForm(forms.ModelForm):
    name       = forms.CharField(max_length=300, help_text="Please enter a name for the task.")
    body       = forms.CharField(widget=forms.Textarea, max_length=3000, help_text="Task Description")
    priority   = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Task
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        fields = ('name', 'body', 'priority')


class FixedModuleForm(forms.ModelForm):
	code = forms.CharField(max_length=60, help_text="Please enter the module code.")
	name = forms.CharField(widget=forms.Textarea, max_length=200)
	description = forms.CharField(widget=forms.Textarea, max_length=3000)

	class Meta:
		model = FixedModule





