from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # view sets, create a set, and delete a set
    (r'^user/$','flashcards.views.list_materials'),
    (r'^create_set/$','flashcards.views.create_set'),
    (r'^user/set/(?P<setID>[-\w]+)/delete_set/$', 'flashcards.views.delete_set'),

    # view all of a set, view a card, add card to a set, modify a card, and delete a card
    (r'^set/(?P<setID>[-\w]+)/$','flashcards.views.list_card'),
    (r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/$','flashcards.views.show_card'),
    (r'^create/(?P<setID>[-\w]+)/$','flashcards.views.create_card'),
    (r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/update/$','flashcards.views.update_card'),
    (r'^set/(?P<setID>[-\w]+)/card/(?P<cardID>[-\w]+)/delete_card/$', 'flashcards.views.delete_card'),

    # review a set
    (r'user/set/(?P<setID>[-\w]+)/start_review/(?P<cardID>[-\w]+)/$', 'flashcards.views.start_review'),
    (r'user/set/(?P<setID>[-\w]+)/review/(?P<cardID>[-\w]+)/(?P<gotRight>[-\w]+)/$', 'flashcards.views.get_next_card'),
    (r'user/set/(?P<setID>[-\w]+)/review/(?P<cardID>[-\w]+)/$', 'flashcards.views.review'),


    # resume
    (r'^$','flashcards.views.resume'),
    (r'^resume/$','flashcards.views.resume'),
    (r'^printable_resume/$', 'flashcards.views.printable_resume'),
    (r'^get_trio/$', 'flashcards.views.get_trio'),

    # other
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    (r'^log_out/$','flashcards.views.log_out'),

    # Social Network analysis:
    (r'^Social_Network_Analysis/$', 'flashcards.views.sna'),
    (r'^get_sna/$', 'flashcards.views.get_sna'),

    (r'^get_learning/$', 'flashcards.views.get_learning'),

    # Meta Tic-Tac-Toe:
    (r'^Meta_Tic-Tac-Toe/$', 'flashcards.views.meta'),
    (r'^get_meta/$', 'flashcards.views.get_meta'),

    (r'^play_meta_ttt/$', 'flashcards.views.play_meta_ttt'),
    (r'^learn_meta_ttt/$', 'flashcards.views.learn_meta_ttt'),
    (r'^play_ttt/$', 'flashcards.views.play_ttt'),
)
