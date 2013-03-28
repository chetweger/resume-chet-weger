'''
Author:
Eli

Description:
These python classes create and describe the database tables needed
for our project.
'''


from django.db import models

# model: userTable
#
# Description
# This model is responsible for storing the information about every user in the system.
#
# Summary of Data Stored
# Each entry in the table will represent a user, and will store
#     - a unique ID number for each user (used by other tables to identify users)
#     - username
#     - email address
#     - password
class userTable(models.Model):
    # userID:   A unique identifier number for each user
    userID = models.AutoField(primary_key=True)

    # userName: A unique string for each user, used to log in and displayed to
    #           other users
    userName = models.CharField(max_length=100)

    # password: A private string used to confirm a user's identity
    password = models.CharField(max_length=100)

    # email:    A string representing the contact email address of each user
    email = models.EmailField(unique=True)

    # get_absolute_url
    # Purpose:  Return a url unique to each user (based on their userID) that
    #           will point to the user's profile page.
    # Input:    self - the userTable object
    # Returns:  A url unique to each user
    def get_absolute_url(self):
        return u"/user/%s/" % self.userID




# model: userSetTable
#
# Description
# This model is responsible for storing the information about every set of flashcards
# that is owned by an individual user.
#
# Summary of Data Stored
# Each entry in the table will represent a set, and will store
#     - a unique ID number for each set (used by other tables to identify sets)
#     - the name of the set
#     - the userTable object of the user that owns the set
class userSetTable(models.Model):
    # setID:    A unique identifier number for each set
    setID = models.AutoField(primary_key=True)

    # setName:  The name of the set, as displayed to users
    setName = models.CharField(max_length=100)

    # owner:    The unique userID for the user that owns the set
    #owner = models.ForeignKey(userTable)

    # get_absolute_url
    # Purpose:  Return a url unique to each set (based on its setID) that
    #           will point to the set's management page.
    # Input:    self - the userSetTable object
    # Returns:  A url unique to each set
    def get_absolute_url(self):
        return u"/set/%s/" % self.setID

class cardTable(models.Model):
    # cardID:   A unique identifier number for each card
    cardID = models.PositiveIntegerField()

    # set:      The unique setID for the set that the card belongs to
    #setID = models.ManyToManyField(userSetTable)
    setID = models.PositiveIntegerField()

    # front:    A string for the data on the front of the card
    front = models.CharField(max_length=140)

    # back:     A string for the data on the back of the card
    back = models.CharField(max_length=140)

    # right:    A boolean for if the user guessed correctly
    right = models.BooleanField(default = False)

    # get_absolute_url
    # Purpose:  Return a url unique to each card (based on its cardID) that
    #           will point to the card's edit page.
    # Input:    self - the cardTable object
    # Returns:  A url unique to each card
    def get_absolute_url(self):
        return u"/set/%s/card/%s/" % (self.setID, self.cardID)
    def __unicode__(self):
        return u"fc(%s,%s)" % (self.front, self.back) #modified from u"Note(%


'''    def get_absolute_url(self):
         return u"/set/%s/card/%s/" % (self.setID,self.cardID)'''


