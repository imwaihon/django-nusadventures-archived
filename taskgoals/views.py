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

from game.views import *

from datetime import datetime



def decode_url(name_url):
    name = name_url.replace('_', ' ')
    return name

def encode_url(name):
    name_url = name.replace(' ', '_')
    return name_url

def get_module_list_all():
    mod_list = Module.objects.all()

    for mod in mod_list:
        mod.url = encode_url(mod.name)

    return mod_list

# Create your views here.


@login_required
def dashboard(request):

    context = RequestContext(request)  
    try:

        user = request.user

        context_dict = {'moduletasks':{}}

        userobj = UserCharacter.objects.get(user=user) 

        context_dict['userchar'] = userobj 

        context_dict['expPercent'] = (float(userobj.expAmt)/get_current_level_exp(userobj.level))*100  #Fixed Percentage as of now

        context_dict['expToLevel'] = get_current_level_exp(userobj.level)


        modules = Module.objects.filter(creator=user, completed=False).order_by('fixedModule')



        for module in modules:
        	tasks = Task.objects.filter(creator=user, module=module, closed=False).order_by('created')[:5]
        	context_dict['moduletasks'][module] = tasks



    except Module.DoesNotExist:
        pass

    return render_to_response('dashboard.html', context_dict, context)



@login_required
def view_all_modules(request):

    context = RequestContext(request)  
    try:

        user = request.user

        context_dict = {'moduletasks':{}}

        userobj = UserCharacter.objects.get(user=user) 

        context_dict['userchar'] = userobj 

        context_dict['expPercent'] = (float(userobj.expAmt)/get_current_level_exp(userobj.level))*100  #Fixed Percentage as of now

        context_dict['expToLevel'] = get_current_level_exp(userobj.level)


        modules = Module.objects.filter(creator=user, completed=False).order_by('fixedModule')



        for module in modules:
            tasks = Task.objects.filter(creator=user, module=module, closed=False).order_by('created')
            context_dict['moduletasks'][module] = tasks



    except Module.DoesNotExist:
        pass

    return render_to_response('tasks.html', context_dict, context)

@login_required
def view_archived_modules(request):

    context = RequestContext(request)  
    try:

        user = request.user

        context_dict = {'modules':{}}

        userobj = UserCharacter.objects.get(user=user) 

        context_dict['userchar'] = userobj 



        modules = Module.objects.filter(creator=user, completed=True).order_by('fixedModule')

        context_dict['modules'] = modules








    except Module.DoesNotExist:
        pass

    return render_to_response('archived_modules.html', context_dict, context)


@login_required
def view_module(request, module_code_url):

    context = RequestContext(request)
    module_code = decode_url(module_code_url)

    context_dict = {'module_code': module_code}

    try:
        fixedmodule = FixedModule.objects.get(code=module_code)

        user = request.user


        module = Module.objects.get(fixedModule=fixedmodule, creator=user)
        context_dict['module'] = module


        tasks = Task.objects.filter(module=module, creator=user, closed=False)
        context_dict['tasks'] = tasks

        history = Task.objects.filter(module=module, creator=user, closed=True)
        context_dict['history'] = history

    except Module.DoesNotExist:
        pass

    return render_to_response('module.html', context_dict, context)




@login_required
def add_module(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = ModuleForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            filledform = form.save(commit=False)
            user = request.user

            try:
                module = Module.objects.get(fixedModule=filledform.fixedModule, creator=user)

            except Module.DoesNotExist:
                filledform.creator = user
                filledform.save()

            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/dashboard/')  
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = ModuleForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('add_module.html', {'form': form}, context)


@login_required
def add_task(request, module_code_url):
    context = RequestContext(request)

    module_code = decode_url(module_code_url)

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            task = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
            	user = request.user

            	fixedmodule = FixedModule.objects.get(code=module_code)

                module = Module.objects.get(fixedModule=fixedmodule, creator=user)

                task.module = module
                task.creator = user

            except Module.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                    return render_to_response( 'add_task.html',
            			{'module_code_url': module_code_url,
             			'module_code': module_code, 'form': form},
             			context)


            # With this, we can then save our new model instance.
            task.save()

            # Now that the page is saved, display the category instead.
            return HttpResponseRedirect('/dashboard/') 
        else:
            print form.errors
    else:
        form = TaskForm()

    return render_to_response( 'add_task.html',
            {'module_code_url': module_code_url,
             'module_code': module_code, 'form': form},
             context)





@login_required
def delete_task(request, del_id):
    context = RequestContext(request)

    if request.method == 'POST':

        try:

            instance = Task.objects.get(id=del_id)

            if (request.user.pk == instance.creator.pk):
                instance.delete()
            else:
                pass

        except Task.DoesNotExist:
            return HttpResponseRedirect('/dashboard/') 


        return HttpResponseRedirect('/dashboard/') 


    else:
        pass

    return render_to_response( 'delete_task.html',
            {'del_id': del_id},
             context)

@login_required
def delete_module(request, module_code_url):
    context = RequestContext(request)
    module_code = decode_url(module_code_url)

    if request.method == 'POST':

        try:

            fixedmodule = FixedModule.objects.get(code=module_code)

            module = Module.objects.get(fixedModule=fixedmodule, creator=request.user)

            tasks = Task.objects.filter(module=module, creator=request.user)

            for task in tasks:
                task.delete()

            module.delete()

        except Module.DoesNotExist:
            return HttpResponseRedirect('/dashboard/') 


        return HttpResponseRedirect('/dashboard/') 


    else:
        pass

    return render_to_response( 'delete_module.html',
            {'module_code_url': module_code_url,
             'module_code': module_code},
             context)


@login_required
def done_task(request, module_code_url, task_id):
    context = RequestContext(request)

    module_code = decode_url(module_code_url)

    if request.method == 'POST':

        try:
            user = request.user

            instance = Task.objects.get(id=task_id)

            if (user.pk == instance.creator.pk and instance.closed == False):
                instance.closed = True
                instance.completed = datetime.now()
                instance.save()
                userchar = UserCharacter.objects.get(user=user)
                userchar.expAmt += 50
                userchar.totalExpAmt += 50
                userchar.taskAmt += 1
                userchar.save()
                check_level_up(userchar)


        except Task.DoesNotExist:
            return HttpResponseRedirect('/dashboard/') 


        return HttpResponseRedirect('/dashboard/') 



    return render_to_response( 'done_task.html',
            {'module_code_url': module_code_url,
             'module_code': module_code, 'task_id': task_id},
             context)

@login_required
def complete_module(request, module_code_url):
    context = RequestContext(request)
    module_code = decode_url(module_code_url)

    if request.method == 'POST':

        try:

            fixedmodule = FixedModule.objects.get(code=module_code)

            module = Module.objects.get(fixedModule=fixedmodule, creator=request.user)

            tasks = Task.objects.filter(module=module, creator=request.user)

            for task in tasks:
                task.delete()

            module.completed = True
            module.save()

        except Module.DoesNotExist:
            return HttpResponseRedirect('/dashboard/') 


        return HttpResponseRedirect('/dashboard/') 


    else:
        pass

    return render_to_response( 'complete_module.html',
            {'module_code_url': module_code_url,
             'module_code': module_code},
             context)