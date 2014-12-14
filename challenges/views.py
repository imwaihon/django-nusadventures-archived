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
from challenges.models import Challenge, UserChallenge, ChallengeTask, UserChallengeTask, ChallengeForm, ChallengeTaskForm, UserChallengeForm, UserChallengeTaskForm

from game.views import *

from datetime import datetime

def decode_url(name_url):
    name = name_url.replace('_', ' ')
    return name

def encode_url(name):
    name_url = name.replace(' ', '_')
    return name_url

# Create your views here.

import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


@login_required
def view_all_challenges(request):

    context = RequestContext(request)  
    try:

        user = request.user

        context_dict = {'challengetasks':{}}

        userobj = UserCharacter.objects.get(user=user) 

        context_dict['userchar'] = userobj 

        context_dict['expPercent'] = (float(userobj.expAmt)/get_current_level_exp(userobj.level))*100  #Fixed Percentage as of now

        context_dict['expToLevel'] = get_current_level_exp(userobj.level)


        userchallenges = UserChallenge.objects.filter(user=user, finished=False).order_by('started')



        for userchallenge in userchallenges:
            tasks = UserChallengeTask.objects.filter(challenge=userchallenge).order_by('challengetask__priority')

            context_dict['challengetasks'][userchallenge] = tasks



    except UserChallenge.DoesNotExist:
        pass

    return render_to_response('challenges.html', context_dict, context)

@login_required
def view_created_challenges(request):

    context = RequestContext(request)  
    try:

        user = request.user

        context_dict = {'challengetasks':{}}

        userobj = UserCharacter.objects.get(user=user) 

        context_dict['userchar'] = userobj 

        context_dict['expPercent'] = (float(userobj.expAmt)/get_current_level_exp(userobj.level))*100  #Fixed Percentage as of now

        context_dict['expToLevel'] = get_current_level_exp(userobj.level)


        userchallenges = Challenge.objects.filter(creator=user).order_by('created')



        for userchallenge in userchallenges:
            tasks = ChallengeTask.objects.filter(challenge=userchallenge)

            context_dict['challengetasks'][userchallenge] = tasks



    except Challenge.DoesNotExist:
        pass

    return render_to_response('created_challenges.html', context_dict, context)


@login_required
def view_challenge(request, challenge_code_url):

    context = RequestContext(request)
    challenge_id = decode_url(challenge_code_url)

    context_dict = {'challenge_id': challenge_id}

    try:
        userchallenge = UserChallenge.objects.get(id=challenge_id, user=request.user)

        user = request.user

        context_dict['challenge'] = userchallenge


        tasks = UserChallengeTask.objects.filter(challenge=userchallenge)
        context_dict['tasks'] = tasks

    except UserChallenge.DoesNotExist:
        pass

    return render_to_response('challenge.html', context_dict, context)


@login_required
def view_created_challenge(request, challenge_code_url):

    context = RequestContext(request)
    challenge_id = decode_url(challenge_code_url)

    context_dict = {'challenge_id': challenge_id}

    try:
        challenge = Challenge.objects.get(id=challenge_id, creator=request.user)

        user = request.user

        context_dict['challenge'] = challenge


        tasks = ChallengeTask.objects.filter(challenge=challenge)
        context_dict['tasks'] = tasks

    except Challenge.DoesNotExist:
        pass

    return render_to_response('created_challenge.html', context_dict, context)

@login_required
def create_challenge(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = ChallengeForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            filledform = form.save(commit=False)
            creator = request.user

            filledform.creator = request.user
            filledform.save()

            userchar = UserCharacter.objects.get(user=request.user)
            userchar.expAmt += 50
            userchar.totalExpAmt += 50
            userchar.contribAmt += 1
            userchar.save()
            check_level_up(userchar)


            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/dashboard/')  
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = ChallengeForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('create_challenge.html', {'form': form}, context)



@login_required
def create_challenge_task(request, challenge_code_url):
    context = RequestContext(request)

    challenge_code = decode_url(challenge_code_url)

    if request.method == 'POST':
        form = ChallengeTaskForm(request.POST)
        user = request.user

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            task = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:

                challenge = Challenge.objects.get(id=challenge_code, creator=request.user)

                task.challenge = challenge
                task.creator = user

            except Challenge.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                    return render_to_response( 'create_challenge_task.html',
                        {'challenge_code_url': challenge_code_url,
                        'challenge_code': challenge_code, 'form': form},
                        context)


            # With this, we can then save our new model instance.
            task.save()

            # Now that the page is saved, display the category instead.
            return HttpResponseRedirect('/created_challenge/'+ challenge_code_url) 
        else:
            print form.errors
    else:
        form = ChallengeTaskForm()

    return render_to_response( 'create_challenge_task.html',
            {'challenge_code_url': challenge_code_url,
             'challenge_code': challenge_code, 'form': form},
             context)


@login_required
def add_challenge(request, challengeid=None):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = UserChallengeForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            filledform = form.save(commit=False)
            user = request.user

            try:
                challenge = Challenge.objects.get(id=challengeid)
                userchallenge = UserChallenge.objects.get(challenge=challenge, user=user)

            except UserChallenge.DoesNotExist:
                filledform.user = user
                challenge = Challenge.objects.get(id=challengeid)
                filledform.challenge = challenge
                filledform.save()

                challenge = Challenge.objects.get(id=challengeid)
                userchallenge = UserChallenge.objects.get(challenge=challenge, user=user)


                tasks = ChallengeTask.objects.filter(challenge=challenge)
                for task in tasks:
                    UserChallengeTask.objects.create(challenge=userchallenge, challengetask=task)



            return HttpResponseRedirect('/challenges/')  
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        challenges = Challenge.objects.filter().order_by('created')[:30]


    return render_to_response('add_challenge.html', {'challenges': challenges}, context)




@login_required
def delete_challenge(request, challenge_code_url):
    context = RequestContext(request)
    challenge_id = decode_url(challenge_code_url)

    if request.method == 'POST':

        try:


            userchallenge = UserChallenge.objects.get(id=challenge_id, user=request.user)

            tasks = UserChallengeTask.objects.filter(challenge=userchallenge)

            for task in tasks:
                task.delete()

            userchallenge.delete()

        except UserChallenge.DoesNotExist:
            return HttpResponseRedirect('/challenges/') 


        return HttpResponseRedirect('/challenges/') 


    else:
        pass

    return render_to_response( 'delete_challenge.html',
            {'challenge_code_url': challenge_code_url,
             'challenge_id': challenge_id},
             context)

@login_required
def delete_challenge_task(request, del_id):
    context = RequestContext(request)

    if request.method == 'POST':

        try:



            task = ChallengeTask.objects.get(id=del_id)

            task.delete()



        except UserChallenge.DoesNotExist:
            return HttpResponseRedirect('/created_challenges/') 


        return HttpResponseRedirect('/created_challenges/') 


    else:
        pass

    return render_to_response( 'delete_challenge_task.html',
             {'del_id': del_id},
             context)


@login_required
def delete_created_challenge(request, del_id):
    context = RequestContext(request)

    if request.method == 'POST':

        try:


            challenge = Challenge.objects.get(id=del_id, creator=request.user)

            tasks = ChallengeTask.objects.filter(challenge=challenge)

            for task in tasks:
                task.delete()

            challenge.delete()

        except Challenge.DoesNotExist:
            return HttpResponseRedirect('/created_challenges/') 


        return HttpResponseRedirect('/created_challenges/') 


    else:
        pass

    return render_to_response( 'delete_created_challenge.html',
            {'del_id': del_id},
             context)


@login_required
def done_challenge_task(request, challenge_code_url, task_id):
    context = RequestContext(request)

    challenge_code = decode_url(challenge_code_url)

    if request.method == 'POST':

        try:
            user = request.user

            instance = UserChallengeTask.objects.get(id=task_id)

            if (user.pk == instance.challenge.user.pk and instance.closed == False):
                instance.closed = True
                instance.completed = datetime.now()
                instance.save()
                userchar = UserCharacter.objects.get(user=user)
                userchar.expAmt += 10
                userchar.totalExpAmt += 10
                userchar.save()
                check_level_up(userchar)


        except UserChallengeTask.DoesNotExist:
            return HttpResponseRedirect('/challenges/') 


        return HttpResponseRedirect('/challenges/') 



    return render_to_response( 'done_challenge_task.html',
            {'challenge_code_url': challenge_code_url,
             'challenge_code': challenge_code, 'task_id': task_id},
             context)

@login_required
def done_challenge(request, challenge_code_url):
    context = RequestContext(request)

    challenge_code = decode_url(challenge_code_url)

    if request.method == 'POST':

        try:
            user = request.user

            instance = UserChallenge.objects.get(id=challenge_code)

            if (user.pk == instance.user.pk and instance.finished == False):
                instance.finished = True
                instance.save()
                userchar = UserCharacter.objects.get(user=user)
                userchar.expAmt += 50
                userchar.totalExpAmt += 50
                userchar.challengeAmt += 1
                userchar.save()
                check_level_up(userchar)


        except UserChallenge.DoesNotExist:
            return HttpResponseRedirect('/challenges/') 


        return HttpResponseRedirect('/challenges/') 



    return render_to_response( 'done_challenge.html',
            {'challenge_code_url': challenge_code_url,
             'challenge_code': challenge_code},
             context)

def search_challenge(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['name','creator__username',])
        
        found_entries = Challenge.objects.filter(entry_query).order_by('-created')

    return render_to_response('search_challenge.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))