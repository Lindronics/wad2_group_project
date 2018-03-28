from django.test import TestCase
from .models import Event, UserProfile
from .forms import *

#Events
##events made in the past present and future
##event location exists
##test event followers

class EventFormTests(TestCase):
    #come back to this because it is fucking up
    #checks to see if the latitude and longitude retrieved match the correct version
    def test_getlatandlong_correct(self):
        #gets a real address with a correct latitude and longitude
        address = "47 killermont road bearsden"
        correctLatandLong = [55.91,-4.32]
        newEvent = NewEventForm()

        #checks to see if the getlantandlong matches correct value
        newEvent.address = address
        newEvent.name = "test"
        newEvent.description = "test"
        newEvent.date_time = "2019-01-01 13:00"
        newEvent.location_info = address
        newEvent.category = Category.objects.filter(name="Test").first()

        #formatting the output
        latandlong = newEvent.getlatandlong()
        latandlong[0] = round(latandlong[0],2)
        latandlong[1] = round(latandlong[1],2)

        #checks done here
        self.assertEqual(latandlong[0], correctLatandLong[0])
        self.assertEqual(latandlong[1], correctLatandLong[1])

    def test_getlatandlong_incorrect(self):
        #gets a non-existent address and ehcks to see if it returns
        # a lat or long
        address = "msamdosamdasodmasod"
        newEvent = NewEventForm()

        #inputting basic details
        newEvent.address = address
        newEvent.name = "test"
        newEvent.description = "test"
        newEvent.date_time = "2019-01-01 13:00"
        newEvent.location_info = address
        newEvent.category = Category.objects.filter(name="Test").first()

        #checks to see if the getlatandlong return any value
        latandlong = newEvent.getlatandlong()
        self.assertIs(len(latandlong) == 0, True)
        


    def test_eventinfuture(self):
        #ensure the datetimes submittable are valid
        address = "47 killermont road bearsden"
        newEvent = NewEventForm()

        #inputting basic details
        newEvent.address = address
        newEvent.name = "test"
        newEvent.description = "test"
        newEvent.date_time = "2019-01-01 13:00"
        newEvent.location_info = address
        newEvent.category = Category.objects.filter(name="Test").first()

        newEvent.clean_date_time()

        

