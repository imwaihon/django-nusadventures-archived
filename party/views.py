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
from party.models import Party, PartyUser, PartyInvite, PartyPost, PartyForm, PartyPostForm, PartyInviteForm

from game.views import *

from datetime import datetime

#create your views here!


@login_required
def view_all_parties(request):

    context = RequestContext(request)  

    try:

        user = request.user

        context_dict = {'parties':{}}

        userobj = UserCharacter.objects.get(user=user) 

        context_dict['userchar'] = userobj 

        context_dict['expPercent'] = (float(userobj.expAmt)/get_current_level_exp(userobj.level))*100  #Fixed Percentage as of now

        context_dict['expToLevel'] = get_current_level_exp(userobj.level)


        parties = PartyUser.objects.filter(user=user)
        partylist = {}

        for party in parties:
        	partylist[party] = party.party

        context_dict['partylist'] = partylist

        context_dict['partyinvites'] = PartyInvite.objects.filter(invited=user)


    except Party.DoesNotExist:
        pass

    return render_to_response('all_party.html', context_dict, context)


@login_required
def view_party(request, party_id):

    context = RequestContext(request)

    context_dict = {'party_id': party_id}

    try:
        party = Party.objects.get(id=party_id)

        user = request.user

        partyuser = PartyUser.objects.get(user=user, party=party)

        partyusers = PartyUser.objects.filter(party=party)

        context_dict['party'] = party
        context_dict['partyusers'] = partyusers

        partyposts = PartyPost.objects.filter(party=party)

        context_dict['partyposts'] = partyposts


    except Party.DoesNotExist or PartyUser.DoesNotExist:
        return HttpResponseRedirect('/all_party/')

    return render_to_response('view_party.html', context_dict, context)

@login_required
def create_party(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = PartyForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            filledform = form.save(commit=False)
            name = filledform.name
            creator = request.user

            filledform.creator = request.user
            filledform.save()

            userchar = UserCharacter.objects.get(user=request.user)
            userchar.expAmt += 50
            userchar.totalExpAmt += 50
            userchar.contribAmt += 1
            userchar.save()
            check_level_up(userchar)


            party = Party.objects.get(creator=request.user, name=name)

            PartyUser.objects.create(user=request.user, party=party)

            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/all_party/')  
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = PartyForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('create_party.html', {'form': form}, context)

@login_required
def create_post(request, party_id):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = PartyPostForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            filledform = form.save(commit=False)

            filledform.poster = request.user
            filledform.party = Party.objects.get(id=party_id)
            filledform.save()

            userchar = UserCharacter.objects.get(user=request.user)
            userchar.expAmt += 10
            userchar.totalExpAmt += 10
            userchar.contribAmt += 1
            userchar.save()
            check_level_up(userchar)



            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/party/'+ party_id)  
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = PartyPostForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('create_post.html', {'form': form , 'party_id': party_id }, context)


@login_required
def delete_party(request, del_id):
    context = RequestContext(request)

    if request.method == 'POST':

        try:

        	party = Party.objects.get(id=del_id, creator=request.user)
        	party.delete()

        except Party.DoesNotExist:
            return HttpResponseRedirect('/party/' + del_id) 


        return HttpResponseRedirect('/all_party/') 


    else:
        pass

    return render_to_response( 'delete_party.html',
            {'del_id': del_id},
             context)

@login_required
def delete_post(request, del_id):
    context = RequestContext(request)

    if request.method == 'POST':

        try:

        	partypost = PartyPost.objects.get(id=del_id, poster=request.user)
        	partypost.delete()

        except PartyPost.DoesNotExist:
        	return HttpResponseRedirect('/all_party/')



        return HttpResponseRedirect('/all_party/') 


    else:
        pass

    return render_to_response( 'delete_post.html',
            {'del_id': del_id},
             context)

@login_required
def invite_party(request, party_id):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = PartyInviteForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.


            try:
            	filledform = form.cleaned_data
            	userinvite = filledform.get('username')

            	party = Party.objects.get(id=party_id)
            	invited = User.objects.get(username=userinvite)

            	PartyInvite.objects.create(party=party, invited=invited)
            except User.DoesNotExist or Party.DoesNotExist:
            	return HttpResponseRedirect('/party'+ party_id)





            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/party/'+ party_id)  
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = PartyInviteForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('invite_party.html', {'form': form , 'party_id': party_id }, context)

@login_required
def accept_party(request, party_id):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':


            try:
            	party = Party.objects.get(id=party_id)
            	invites = PartyInvite.objects.filter(party=party, invited=request.user)

            	for invite in invites:
            		invite.delete()

            	PartyUser.objects.get(user=request.user, party=party)

            	

            except PartyUser.DoesNotExist:
            	PartyUser.objects.create(user=request.user, party=party)




            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/party/'+ party_id)  

    else:
        # If the request was not a POST, display the form to enter details.

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    	return render_to_response('accept_party.html', {'party_id': party_id }, context)


@login_required
def decline_party(request, party_id):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':



        party = Party.objects.get(id=party_id)
        invites = PartyInvite.objects.filter(party=party, invited=request.user)

        for invite in invites:
            invite.delete()








        # Now call the index() view.
        # The user will be shown the homepage.
        return HttpResponseRedirect('/all_party/')  

    else:
        # If the request was not a POST, display the form to enter details.

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
        return render_to_response('decline_party.html', {'party_id': party_id }, context)


