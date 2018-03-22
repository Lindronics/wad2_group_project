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


def nearby_locations(latitude, longitude, radius, max_results=100, use_miles=True):
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
    AS distance FROM Whats_On_Dot_Com_Event WHERE distance < %d
    ORDER BY distance LIMIT 0 , %d;""" % (distance_unit, latitude, longitude, latitude, int(radius), max_results)
    cursor.execute(sql)
    ids = [row[0] for row in cursor.fetchall()]
    #I have ids of all objects
    #and return the relevant object
    return Event.objects.filter(id__in=ids)
#calling wrong as 55.8 is assigned to self
#print (Event.objects.filter(latitude__isnull=False))
print (nearby_locations(55.8, -4.2, 10, 50))

"""
    
    #What PHP does in the example :
    #the PHP code first initializes a new XML document and creates the "markers" parent node. It then connects to the database, executes a SELECT * (select all) query on the markers table, and iterates through the results.
    #For each row in the table (each location), the code creates a new XML node with the row attributes as XML attributes, and appends it to the parent node. The last part of code then dumps the XML to the browser screen.

    #What the XML is used for:
    #
get_queryset()

#Set this up so it takes data from fields as in django example then returns a json thingmy i think
"""
