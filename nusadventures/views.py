from django.shortcuts import render

# For html template import
from django.template import RequestContext
from django.shortcuts import render_to_response

# HttpResponse import 
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User


from taskgoals.models import Module, Task, ModuleForm, TaskForm, FixedModule
from game.models import UserCharacter, Achievement, UserAchievement, UserCharacterForm, AchievementForm, UserAchievementForm


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)


    context_dict = {}

    return render_to_response('index.html', context_dict, context)



def about(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)


    context_dict = {}

    return render_to_response('about.html', context_dict, context)


