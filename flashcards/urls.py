from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$','flashcards.views.resume'),
    (r'^get_trio/$', 'flashcards.views.get_trio'),
    (r'^set/(?P<setID>[-\w]+)/$','flashcards.views.list_card'),

    (r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/delete_card/$', 'flashcards.views.delete_card'),

    (r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/$','flashcards.views.show_card'),
    (r'^create/(?P<setID>[-\w]+)/$','flashcards.views.create_card'),
    (r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/update/$','flashcards.views.update_card'),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),

    (r'^user/$','flashcards.views.list_materials'),

    (r'^user/set/(?P<setID>[-\w]+)/delete_set/$', 'flashcards.views.delete_set'),


    (r'^log_out/$','flashcards.views.log_out'),
    (r'^create_set/$','flashcards.views.create_set'),

    (r'user/set/(?P<setID>[-\w]+)/review/(?P<cardID>[-\w]+)/(?P<gotRight>[-\w]+)/$', 'flashcards.views.get_next_card'),
    (r'user/set/(?P<setID>[-\w]+)/review/(?P<cardID>[-\w]+)/$', 'flashcards.views.review'),

)
