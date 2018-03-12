import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project_whats_on.settings")


import django

from django.apps import apps
from django.conf import settings

if not apps.ready and not settings.configured:
    django.setup()

from whats_on_dot_com.models import *
#from django.contrib.auth.models import User

#What I want to do in SQL
#SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) )
#* cos( radians( lng ) - radians(-122) ) + sin( radians(37) )
#* sin( radians( lat ) ) ) )
#AS distance FROM markers HAVING distance < 25 ORDER BY distance;

def extract_query():
    #Using raw sql here as is easier than trying to convert
    #ideally convert as raw sql is somewhat more vulnerable
    #see here for details https://docs.djangoproject.com/en/2.0/topics/db/sql/
    "Change the distance 25 to a variable thats passed in"
    "Change following hard coded search loc to passed in users loc"
    search_lat = 55.8
    search_long = -4.2
    #query = Event.objects.raw('SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians(-122) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM Event HAVING distance < 25 ORDER BY distance')
    for event in Event.objects.raw('SELECT id, ( 3959 * acos( cos( radians(%s) ) * cos( radians( latitude ) ) * cos( radians( %s ) - radians(search_long) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM Event HAVING distance < 25 ORDER BY distance', [search_lat, search_long]):
        print (event)

    #test = Event.objects.raw('SELECT * FROM Event')
    #Use raw sql query to extract relevant events
    #write events to json
    #
    #test
    #print (test)

    #Cant use php with django
    #so use python instead
    #NB: The markers table is the Events table in our implementation
    
    #What PHP does in the example :
    #the PHP code first initializes a new XML document and creates the "markers" parent node. It then connects to the database, executes a SELECT * (select all) query on the markers table, and iterates through the results.
    #For each row in the table (each location), the code creates a new XML node with the row attributes as XML attributes, and appends it to the parent node. The last part of code then dumps the XML to the browser screen.

    #What the XML is used for:
    #
extract_query()

#Set this up so it takes data from fields as in django example then returns a json thingmy i think
