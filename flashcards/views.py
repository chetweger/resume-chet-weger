'''
General Description:
Entering a certain url (into a browser) calls a view function
based on the mappings described in the urls.py file.
These functions take a request and url
digits as parameters.  They interface with
models and templates.
'''

from django.core.context_processors import csrf
from models import cardTable
from models import userSetTable
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseServerError, HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.core.servers.basehttp import FileWrapper
import os, tempfile, zipfile
import settings_dev

from secrets import FB_CLIENT_SECRET, FB_CLIENT_ID
from urllib import urlopen
import json

HOME = os.getcwd()
MAX_SIZE_SETS = 100

def play_ttt(request):
  return render(request, 'fc/TTT.html')

def play_meta_ttt(request):
  return render(request, 'fc/Meta.html')

def learn_meta_ttt(request):
  return render(request, 'fc/LearnMeta.html')

def sna(request):
  '''returns sna html'''
  return render(request, 'fc/SNA.html')

def get_sna(request):
  '''return sna.py project '''
  response = getFileResponse('sna.py')
  return response

def meta(request):
  '''returns AI meta-tic-tac-toe '''
  return render(request, 'fc/Meta_Tic-Tac-Toe.html')

def get_meta(request):
  '''returns AI meta-tic-tac-toe '''
  response = getFileResponse('meta.py')
  return response

def get_learning(request):
  ''' returns learning.py '''
  response = getFileResponse('learning.py')
  return response

def getFileResponse(filename):
  '''return a file attachment for given filename '''
  fullFN = HOME + '/media/' + filename
  trio = open(fullFN, 'r')
  list = trio.readlines()
  result = reduce( (lambda x, y: x+y), list)
  response = HttpResponse(result)
  response['Content-Disposition'] = 'attachment; filename = ' + fullFN
  return response

def get_trio(request):
  '''return file response '''
  print "WAS called trololol"
  response = getFileResponse('trio.py')
  print "was reached i dunno"
  return response

def printable_resume(request):
  '''show printable resume '''
  return render(request, 'fc/printable_resume.html')

def resume(request):
  '''show my resume '''
  red = HttpResponsePermanentRedirect('/media/Chet_Weger.pdf')
  return red

def list_card(request, setID):
  '''lists card in current set '''
  cardList = cardTable.objects.filter(setID = setID).order_by('cardID')[0:MAX_SIZE_SETS]
  assert len(cardList) == len(cardTable.objects.filter(setID=setID)) #defensive programming
  url_create = "/create/" + str(setID) + "/"
  return render(request, 'fc/list.html', {'card_list': cardList, 'url_create': url_create,})

def faceb_signup(request):
  if request.method == 'GET':
    code = request.GET.get('code', '')
    print 'code is ', code
    url_token_request = ('https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s'
                         % (FB_CLIENT_ID,
                           'http://localhost/faceb_signup/',
                           FB_CLIENT_SECRET,
                           code,
                           )
                        )
    response = urlopen(url_token_request).read()
    print 'response is ', response
    access_token, expires = response.replace('access_token=', '').split('&expires=')
    print 'response is ', response
    print 'access token is ', access_token
    url = ('https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials'
           % (FB_CLIENT_ID, FB_CLIENT_SECRET)
          )

    print 'new url is ',  url
    resp = urlopen(url).read()
    resp = resp.replace('access_token=', '')
    print 'response is ', resp
    base = 'https://graph.facebook.com/debug_token'
    url = base + '?input_token=%s&access_token=%s' % (access_token, resp)
    print 'url is ', url
    final_oauth_response = urlopen(url).read()
    faceb_user_id = json.loads(final_oauth_response)['data']['user_id']
    print 'final_oauth_response is ', final_oauth_response

    facebook_url = 'https://graph.facebook.com/' + str(faceb_user_id) + '?access_token=' + access_token
    facebook_str = urlopen(facebook_url).read()
    print 'facebook_info is', facebook_str
    facebook_info = json.loads(facebook_str)
    print facebook_info
    return render(request, "asdfasdfasdfasdfas")



def show_card(request, setID, cardID):
  '''shows details of a card '''
  list_url = "/set/" + setID + "/"
  return render(request, 'fc/fc_detail.html', {'object': cardTable.objects.filter(setID=setID).get(cardID=cardID), 'list_url': list_url,})

def delete_card(request, setID, cardID):
  deleteMe = cardTable.objects.filter(setID=setID).get(cardID = cardID)
  deleteMe.delete()
  return HttpResponsePermanentRedirect('/set/'+str(setID)+'/')

def create_card(request, setID):
  '''Creates a new card '''
  if request.method == "POST":
    post = request.POST.copy()
    if post.has_key('front') and post.has_key('back'):
      order = len(cardTable.objects.filter(setID = setID))  #later must check for int
      if cardTable.objects.filter(cardID=order).filter(setID=setID).count() == 0:
        if len(cardTable.objects.all()) <= MAX_SIZE_SETS:
          front = post['front']
          back = post['back']
          new_flashcard = cardTable.objects.create(cardID=order, setID=setID, front=front, back=back)
          return HttpResponsePermanentRedirect('/set/%s'% setID)
        else: error_msg = u"Maximum size of set reached.  Please create a new set to add more flashcards."
      else: error_msg = u"Please enter an integer value."
    else: error_msg = u"Insufficient POST data (enter in forms)"
  else: error_msg = u"No POST data sent."
  return HttpResponseServerError(error_msg)

def update_card(request, setID, cardID):
  '''allows card to be modified '''
  if request.method == "POST":
    post = request.POST.copy()
    flashcard = cardTable.objects.filter(setID=setID).get(cardID=cardID)
    if post.has_key('front'):
      flashcard.front = post['front']
    if post.has_key('back'):
      flashcard.back = post['back']
    flashcard.save()
    return HttpResponseRedirect(flashcard.get_absolute_url())
  else: error_msg = u"No POST data sent."
  return HttpResponseServerError(error_msg)

def list_materials(request):
  '''lists the contents of a set '''
  setList = userSetTable.objects.order_by('setID')[0:MAX_SIZE_SETS]
  assert len(setList) == len(userSetTable.objects.all())
  print "length of setList", len(setList), "length of all", len(userSetTable.objects.all())
  trio_url = '/get_trio/'
  return render(request, 'fc/user.html', {'set_list': setList, 'trio_url': trio_url,})

def delete_set(request, setID):
  '''deletes the current set '''
  deleteMe = userSetTable.objects.get(setID = setID)
  deleteCards = cardTable.objects.filter(setID = setID)
  for delCard in deleteCards:
    delCard.delete()
  deleteMe.delete()
  return HttpResponsePermanentRedirect('/user/')

def create_set(request):
  '''creates a new set '''
  if request.method == "POST":
    post = request.POST.copy()
    if (post.has_key('setName') and len(post['setName']) > 0 and
          len(userSetTable.objects.filter(setName = post['setName'])) == 0):
      if len(userSetTable.objects.all()) < MAX_SIZE_SETS:
        order = len(userSetTable.objects.all())
        setName = post['setName']
        new_set = userSetTable.objects.create(setID=order, setName=setName)
        return HttpResponsePermanentRedirect('/user/')
      else: error_msg = u"Maximum size of sets reached.  Please delete some of you sets."
    else: error_msg = u"Enter unique and valid set name"
  else: error_msg = u"No POST data sent."
  return HttpResponseServerError(error_msg)

def log_out(request):
  '''user functionality not implemented yet '''
  logout(request)
  return HttpResponseServerError("User accounts not implemented yet.")

def start_review(request, setID, cardID, gotRight):
  '''sets all cards as unreviewed when we start a review session
(this is a wrapper function)
  '''
  allCards = cardTable.objects.filter(setID = setID)
  for card in allCards:
    # Now that we are finish with set, reset right values
    card.right = False
    card.save()
  return get_next_card(request, setID, cardID, gotRight)

def get_next_card(request, setID, cardID, gotRight):
  '''Handles the result of calling next card
Calls the review function
  '''
  setID = int(setID)
  cardID = int(cardID)
  if eval(gotRight):
    done_flashcard = cardTable.objects.get(setID=setID, cardID=cardID)
    done_flashcard.right = True
    done_flashcard.save()
  cardsLeft = cardTable.objects.filter(setID=setID, right=False)
  if(cardsLeft):
    cardsLeft = cardsLeft.order_by('cardID')
  if len(cardsLeft) == 0:
    return review(request, setID, -1)
  elif len(cardsLeft) == 1:
    return review(request, setID, cardsLeft[0].cardID)
  elif len(cardsLeft) > 1:
    print "cardID", cardID
    cardsAfter = cardsLeft[cardID+1: MAX_SIZE_SETS]
    if len(cardsAfter) > 0:
      # try to find a card with a larger cardID
      print "cardAfter", cardsAfter
      return review(request, setID, cardsAfter[0].cardID)
    else:
      # pick card with smallest cardID
      print "CardsLeft", cardsLeft
      return review(request, setID, cardsLeft[0].cardID)

def review(request, setID, cardID):
  if cardID == -1:
    allCards = cardTable.objects.filter(setID=setID)
    for card in allCards:
      # Now that we are finish with set, reset 'right' values
      card.right = False
      card.save()
    return render(request, 'fc/congrats.html')
  nextCard = cardTable.objects.get(setID=setID, cardID = cardID, right=False)
  return render(request, 'fc/review.html', {'flashcard': nextCard,})
