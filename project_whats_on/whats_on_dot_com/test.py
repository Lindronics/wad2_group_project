from django.test import TestCase
from .models import Event, UserProfile
from .forms import *



#Things to test
#Users
##user following system
class UserTests(TestCase):
    def test_usersarefollowing_correct(self):
        user1 = User(username = "test1")
        user2 = User(username = "test2")
        u1 = UserProfile(user = user1)
        u2 = UserProfile(user = user2)
        
        u1.follows.add(u2)


    


#Events
##events made in the past present and future
##event location exists
##test event followers

class EventFormTests(TestCase):
    #come back to this because it is fucking up
    #checks to see if the latitude and longitude retrieved match the correct version
    def test_getlatandlong_correct(self):
        address = "47 killermont road bearsden"
        correctLatandLong = [55.910,-4,3165]
        newEvent = NewEventForm()

        
        newEvent.address = address
        newEvent.name = "test"
        newEvent.description = "test"
        newEvent.date_time = "2019-01-01 13:00"
        newEvent.location_info = address
        newEvent.category = Category.objects.filter(name="Test").first()

        newEvent.cleaned_data["address"] = address
        newEvent.is_valid()
        latandlong = newEvent.getlatandlong()
        print(latandlong)
        
