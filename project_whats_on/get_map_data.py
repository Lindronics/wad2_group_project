import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project_whats_on.settings")


import django
import math

from django.apps import apps
from django.conf import settings

if not apps.ready and not settings.configured:
    django.setup()

from whats_on_dot_com.models import *

#https://stackoverflow.com/questions/1916953/filter-zipcodes-by-proximity-in-django-with-the-spherical-law-of-cosines
'3rd answer down'

def nearby_locations(self, latitude, longitude, radius, max_results=100, use_miles=True):
    if use_miles:
        distance_unit = 3959
    else:
        distance_unit = 6371

    from django.db import connection, transaction
    from project_whats_on import settings
    cursor = connection.cursor()
    #print(settings.DATABASES['default']['ENGINE'])
    #if settings.DATABASE_ENGINE == 'sqlite3':
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        connection.connection.create_function('acos', 1, math.acos)
        connection.connection.create_function('cos', 1, math.cos)
        connection.connection.create_function('radians', 1, math.radians)
        connection.connection.create_function('sin', 1, math.sin)

    sql = """SELECT id, (%f * acos( cos( radians(%f) ) * cos( radians( latitude ) ) *
    cos( radians( longitude ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( latitude ) ) ) )
    AS distance FROM EVENT WHERE distance < %d
    ORDER BY distance LIMIT 0 , %d;""" % (distance_unit, latitude, longitude, latitude, int(radius), max_results)
    cursor.execute(sql)
    ids = [row[0] for row in cursor.fetchall()]

    return self.filter(id__in=ids)

nearby_locations(self, 55.8, -4.2, 10, 50)
#What I want to do in SQL
#SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) )
#* cos( radians( lng ) - radians(-122) ) + sin( radians(37) )
#* sin( radians( lat ) ) ) )
#AS distance FROM markers HAVING distance < 25 ORDER BY distance;
"""
def get_queryset():
    #Using raw sql here as is easier than trying to convert
    #ideally convert as raw sql is somewhat more vulnerable
    #see here for details https://docs.djangoproject.com/en/2.0/topics/db/sql/
    "Change the distance 25 to a variable thats passed in"
    "Change following hard coded search loc to passed in users loc"
    search_lat = 55.8   #get from form
    search_long = -4.2 #get from form
    desired_dist = 10 #get from form
    
    
    #query = Event.objects.raw('SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians(-122) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM Event HAVING distance < 25 ORDER BY distance')
    """

    #for event in Event.objects.raw('SELECT id, ( 3959 * acos( cos( radians(%s) ) * cos( radians( latitude ) ) * cos( radians( %s ) - radians(search_long) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM Event HAVING distance < 25 ORDER BY distance', [search_lat, search_long]):
     #   print (event)

"""


    
    #What PHP does in the example :
    #the PHP code first initializes a new XML document and creates the "markers" parent node. It then connects to the database, executes a SELECT * (select all) query on the markers table, and iterates through the results.
    #For each row in the table (each location), the code creates a new XML node with the row attributes as XML attributes, and appends it to the parent node. The last part of code then dumps the XML to the browser screen.

    #What the XML is used for:
    #
get_queryset()

#Set this up so it takes data from fields as in django example then returns a json thingmy i think
"""
