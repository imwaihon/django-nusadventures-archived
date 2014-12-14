from django.contrib import admin
from taskgoals.models import Module, Task, FixedModule
from nusadventures.models import UserProfile


# Register your models here.
admin.site.register(FixedModule)
admin.site.register(Module)
admin.site.register(Task)

#admin.site.register(UserProfile)


