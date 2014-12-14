from django.conf.urls import patterns, include, url

import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nusadventures.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.index, name='index'),

    url(r'^about/', views.about, name='about'),
    
    #taskgoals

    url(r'^dashboard/', 'taskgoals.views.dashboard', name='dashboard'),
    url(r'^tasks/', 'taskgoals.views.view_all_modules', name='view_all_modules'),
    url(r'^archived/', 'taskgoals.views.view_archived_modules', name='view_archived_modules'),

    url(r'^add_module/', 'taskgoals.views.add_module', name='add_module'),
    url(r'^(?P<del_id>\w+)/delete_task/', 'taskgoals.views.delete_task', name='delete_task'),

    url(r'^module/(?P<module_code_url>\w+)$', 'taskgoals.views.view_module', name='view_module'),
    url(r'^module/(?P<module_code_url>\w+)/add_task/', 'taskgoals.views.add_task', name='add_task'),
    url(r'^(?P<module_code_url>\w+)/delete_module', 'taskgoals.views.delete_module', name='delete_module'),
    url(r'^complete_module/(?P<module_code_url>\w+)', 'taskgoals.views.complete_module', name='complete_module'),

    url(r'^(?P<module_code_url>\w+)/(?P<task_id>\w+)/done_task', 'taskgoals.views.done_task', name='done_task'),

    #challenges

    url(r'^challenges/', 'challenges.views.view_all_challenges', name='view_all_challenges'),
    url(r'^created_challenges/', 'challenges.views.view_created_challenges', name='view_created_challenges'),


    url(r'^create_challenge/', 'challenges.views.create_challenge', name='create_challenge'),
    url(r'^create_challenge_task/(?P<challenge_code_url>\w+)', 'challenges.views.create_challenge_task', name='create_challenge_task'),
    url(r'^created_challenge/(?P<challenge_code_url>\w+)', 'challenges.views.view_created_challenge', name='view_created_challenge'),

    url(r'^add_challenge/(?P<challengeid>\w+)', 'challenges.views.add_challenge', name='add_challenge'),    
    url(r'^add_challenge/', 'challenges.views.add_challenge', name='add_challenge'),
    url(r'^search_challenge/', 'challenges.views.search_challenge', name='search_challenge'),
    

    url(r'^challenge/(?P<challenge_code_url>\w+)$', 'challenges.views.view_challenge', name='view_challenge'),

    url(r'^delete_challenge_task/(?P<del_id>\w+)', 'challenges.views.delete_challenge_task', name='delete_challenge_task'),
    url(r'^(?P<challenge_code_url>\w+)/delete_challenge', 'challenges.views.delete_challenge', name='delete_challenge'),
    url(r'^delete_created_challenge/(?P<del_id>\w+)', 'challenges.views.delete_created_challenge', name='delete_created_challenge'),

    url(r'^done_challenge/(?P<challenge_code_url>\w+)', 'challenges.views.done_challenge', name='done_challenge'),
    url(r'^done_challenge_task/(?P<challenge_code_url>\w+)/(?P<task_id>\w+)', 'challenges.views.done_challenge_task', name='done_challenge_task'),


    #party
    url(r'^all_party/', 'party.views.view_all_parties', name='view_all_parties'),
    url(r'^party/(?P<party_id>\w+)$', 'party.views.view_party', name='view_party'),
    url(r'^create_party/', 'party.views.create_party', name='create_party'),
    url(r'^create_post/(?P<party_id>\w+)$', 'party.views.create_post', name='create_post'),
    url(r'^delete_party/(?P<del_id>\w+)', 'party.views.delete_party', name='delete_party'),
    url(r'^delete_post/(?P<del_id>\w+)', 'party.views.delete_post', name='delete_post'),

    url(r'^accept_party/(?P<party_id>\w+)', 'party.views.accept_party', name='accept_party'),
    url(r'^decline_party/(?P<party_id>\w+)', 'party.views.decline_party', name='decline_party'),
    url(r'^invite_party/(?P<party_id>\w+)', 'party.views.invite_party', name='invite_party'),

    #game
    url(r'^leaderboard/', 'game.views.leaderboard', name='leaderboard'),
    url(r'^profile_card/(?P<username>\w+)', 'game.views.profile_card', name='profile_card'),
    url(r'^upvote/(?P<username>\w+)', 'game.views.upvote', name='upvote'),
    url(r'^edit_description/(?P<username>\w+)', 'game.views.edit_description', name='edit_description'),



    

)
