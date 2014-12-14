from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# For html template import
from django.template import RequestContext
from django.shortcuts import render_to_response

# HttpResponse import 
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User

from taskgoals.models import Module, Task, ModuleForm, TaskForm, FixedModule
from game.models import UserCharacter, Achievement, UserAchievement, UserCharacterForm, AchievementForm, UserAchievementForm

# Create your views here.

def check_level_up(userchar):
	while userchar.expAmt >= get_current_level_exp(userchar.level):
		userchar.expAmt -= get_current_level_exp(userchar.level)
		userchar.level += 1
	userchar.save()


def get_current_level_exp(level):
	return levels_store[level]


levels_store = {1: 200, 2: 400, 3: 600, 4: 800, 5: 1000, 6: 1200, 7: 1400, 8: 1600, 9: 1800, 10: 2000, 11: 2200, 12: 2400, 13: 2600, 14: 2800, 15: 3000, 16: 3200, 17: 3400, 18: 3600, 19: 3800, 20: 4000, 21: 4200, 22: 4400, 23: 4600, 24: 4800, 25: 5000, 26: 5200, 27: 5400, 28: 5600, 29: 5800, 30: 6000, 31: 6200, 32: 6400, 33: 6600, 34: 6800, 35: 7000, 36: 7200, 37: 7400, 38: 7600, 39: 7800, 40: 8000, 41: 8200, 42: 8400, 43: 8600, 44: 8800, 45: 9000, 46: 9200, 47: 9400, 48: 9600, 49: 9800, 50: 10000, 51: 10200, 52: 10400, 53: 10600, 54: 10800, 55: 11000, 56: 11200, 57: 11400, 58: 11600, 59: 11800, 60: 12000, 61: 12200, 62: 12400, 63: 12600, 64: 12800, 65: 13000, 66: 13200, 67: 13400, 68: 13600, 69: 13800, 70: 14000, 71: 14200, 72: 14400, 73: 14600, 74: 14800, 75: 15000, 76: 15200, 77: 15400, 78: 15600, 79: 15800, 80: 16000, 81: 16200, 82: 16400, 83: 16600, 84: 16800, 85: 17000, 86: 17200, 87: 17400, 88: 17600, 89: 17800, 90: 18000, 91: 18200, 92: 18400, 93: 18600, 94: 18800, 95: 19000, 96: 19200, 97: 19400, 98: 19600, 99: 19800, 100: 20000}


@login_required
def leaderboard(request):

    context = RequestContext(request)  
    try:
    	context_dict = {}
        user = request.user


        userobj = UserCharacter.objects.get(user=user) 

        context_dict['userchar'] = userobj 

        context_dict['expPercent'] = (float(userobj.expAmt)/get_current_level_exp(userobj.level))*100  #Fixed Percentage as of now

        context_dict['expToLevel'] = get_current_level_exp(userobj.level)

        top50 = UserCharacter.objects.order_by('-totalExpAmt')[:50]

        i = 1
        context_dict['top50'] = {}

        for entry in top50:
        	context_dict['top50'][i] = entry
        	i += 1






    except UserCharacter.DoesNotExist:
        pass

    return render_to_response('leaderboard.html', context_dict, context)



def profile_card(request, username):

    context = RequestContext(request)  
    try:
    	context_dict = {}

    	user = User.objects.get(username=username)

    	context_dict['profileuser'] = user

        userobj = UserCharacter.objects.get(user=user) 

        context_dict['userchar'] = userobj 

        context_dict['expPercent'] = (float(userobj.expAmt)/get_current_level_exp(userobj.level))*100  #Fixed Percentage as of now

        context_dict['expToLevel'] = get_current_level_exp(userobj.level)

        completed = Module.objects.filter(creator=user, completed=True)

        context_dict['completed'] = completed

        active = Module.objects.filter(creator=user, completed=False)

        context_dict['active'] = active




    except User.DoesNotExist:
        pass

    return render_to_response('profile_card.html', context_dict, context)

@login_required
def upvote(request, username):
    context = RequestContext(request)

    context_dict = {}



    if request.method == 'GET':

        try:


            user = User.objects.get(username=username)

            context_dict['profileuser'] = user

            userobj = UserCharacter.objects.get(user=user) 

            context_dict['userchar'] = userobj 

            userobj.upvoteAmt += 1
            userobj.save()

        except User.DoesNotExist:
            pass


        return HttpResponseRedirect('/profile_card/'+username) 



    return render_to_response( "",
            context_dict,
             context)


@login_required
def edit_description(request, username):
    context = RequestContext(request)

    context_dict = {}

    if request.user.username != username:
        return HttpResponseRedirect('/dashboard/')


    user = User.objects.get(username=username)

    context_dict['profileuser'] = user

    userobj = UserCharacter.objects.get(user=user) 

    context_dict['userchar'] = userobj 

    context_dict['description'] = userobj.description

    if request.method == 'POST':

        try:

            userobj.description = request.POST['describe']
            userobj.save()




        except User.DoesNotExist:
            pass


        return HttpResponseRedirect('/profile_card/'+username) 




    return render_to_response( "edit_description.html",
            context_dict,
             context)