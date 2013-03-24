'''
General Description:
Entering a certain url (into a browser) calls a view function
based on the mappings described in the urls.py file.
These functions take a request and url
digits as parameters.  They interface with
models and templates.

Authors:
Chet authored the first five view functions.
Michael authored the last four view functions.
'''

from django.core.context_processors import csrf
from models import cardTable
from models import userSetTable
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth import logout

#lists card in current set
def list_card(request, setID):
    print setID, type(setID)
    cardList = cardTable.objects.filter(setID = setID).order_by('cardID')
    url_create = "/create/" + str(setID) + "/"
    return render(request, 'fc/list.html', {'card_list': cardList, 'url_create': url_create,})

#shows details of a card
def show_card(request, setID, cardID):
    list_url = "/set/" + setID + "/"
    return render(request, 'fc/fc_detail.html', {'object': cardTable.objects.filter(setID=setID).get(cardID=cardID), 'list_url': list_url,})

def delete_card(request, setID, cardID):
    deleteMe = cardTable.objects.filter(setID=setID).get(cardID = cardID)
    deleteMe.delete()
    return HttpResponsePermanentRedirect('/set/'+str(setID)+'/')

def create_card(request, setID):
    if request.method == "POST":
        post = request.POST.copy()
        if post.has_key('order') and post.has_key('front') and post.has_key('back'):
            if (post['order'].isdigit()):
                order = int(post['order'])  #later must check for int
                if cardTable.objects.filter(cardID=order).filter(setID=setID).count() == 0:
                    front = post['front']
                    back = post['back']
                    new_flashcard = cardTable.objects.create(cardID=order, setID=setID, front=front, back=back)
                    return HttpResponsePermanentRedirect('/set/%s'% setID)
                else: error_msg = u"Order already in use."
            else: error_msg = u"Please enter an integer value."
        else: error_msg = u"Insufficient POST data (enter in forms)"
    else: error_msg = u"No POST data sent."
    return HttpResponseServerError(error_msg)

def update_card(request, setID, cardID):
    if request.method == "POST":
        post = request.POST.copy()
        flashcard = cardTable.objects.filter(setID=setID).get(cardID=cardID)
        if post.has_key('order'):
            if post['order'].isdigit():
                order = int(post['order'])
                if flashcard.cardID != order:
                    if cardTable.objects.filter(setID=setID).filter(cardID=order).count() == 0:
                        flashcard.cardID = order
                    else:
                        error_msg = u"cardID/order already taken."
                        return HttpResponseServerError(error_msg)
            else: return HttpResponseServerError(u"Please enter an integer value.")
        if post.has_key('front'):
            flashcard.front = post['front']
        if post.has_key('back'):
            flashcard.back = post['back']
        flashcard.save()
        return HttpResponseRedirect(flashcard.get_absolute_url())
    else: error_msg = u"No POST data sent."
    return HttpResponseServerError(error_msg)

#Michael's:
def list_materials(request):
    setList = userSetTable.objects.order_by('setID')
#    groupList = userGroupTable.object.order_by('groupID')
    return render(request, 'fc/user.html', {'set_list': setList,})

def delete_set(request, setID):
    deleteMe = userSetTable.objects.get(setID = setID)
    deleteMe.delete()
    return HttpResponsePermanentRedirect('/user/')

#def leave_group(request, groupID):
#    deleteMe = userGroupTable.objects.get(groupID = groupID)
#    deleteMe.delete()
#    return HttpResponsePermanentRedirect('/user/')

def create_set(request):
    if request.method == "POST":
        post = request.POST.copy()
        if post.has_key('setName'):
            order = len(userSetTable.objects.all())
            setName = post['setName']
            new_set = userSetTable.objects.create(setID=order, setName=setName)
            return HttpResponsePermanentRedirect('/user/')
        else: error_msg = u"Insufficient POST data (enter in forms)"
    else: error_msg = u"No POST data sent."
    return HttpResponseServerError(error_msg)

def log_out(request):
    logout(request)
    HttpResponseRedirect('/home/')
