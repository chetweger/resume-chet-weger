from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#Chet's:
	(r'^set/(?P<setID>[-\w]+)/$','flashcards.views.list_card'),

	(r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/delete_card/$', 'flashcards.views.delete_card'),

	(r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/$','flashcards.views.show_card'),
	(r'^create/(?P<setID>[-\w]+)/$','flashcards.views.create_card'),
	(r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/update/$','flashcards.views.update_card'),
	
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),

	#Michael's
	(r'^$','flashcards.views.list_materials'),
	(r'^user/$','flashcards.views.list_materials'),

	(r'^user/set/(?P<setID>[-\w]+)/delete_set/$', 'flashcards.views.delete_set'),
	
#	(r'^user/group/(?P<groupID>[-\w]+)/leave_group/$', 'flashcards.views.leave_group'),

	(r'^user/log_out/','flashcards.views.log_out'),
	(r'^create_set/$','flashcards.views.create_set'),
)
