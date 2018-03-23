from django import template
#THESE TEMPLATES FOR NEARBY_LOC TO WORK PROBABLY
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project_whats_on.settings")

import django
import math

from django.apps import apps
from django.conf import settings

if not apps.ready and not settings.configured:
    django.setup()

from whats_on_dot_com.models import *
#END OF THOSE ONES
#datetime import for filter by date
from datetime import datetime as dt


register = template.Library()

@register.simple_tag
def test_tag(value):
    value = int(value)
    value += 10
    return value

#this should be a tag not a filter...
@register.simple_tag
def search(lat, lng, people, radius, year, month, day, hour, minute, category, search_term ):
    #parameters is a list object containing
    #people (can be added at later stage when i get it)
    #radius from the point
    #Max date from now to look (eg. 1 month away)
    #category (can be done later)
    #what the event name should contain
    #parameters looks like
    #radii in km
    #[Null, 30, (YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, MILLISECOND),
    #NULL, (NULL OR STRING)]
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

    #filter for people -TODO

    #filter for radius
    semi_filtered = nearby_locations(lat, lng, radius, 100, False)

    #filter for date from now
    semi_filtered = semi_filtered.filter(date__range=[dt.now(), (year, month, day, hour, minute)])

    #filter for category - TODO

    #filter for name contains
    if not parameters[4] == None:
        filtered = semi_filtered.filter(name__icontains=search_term)
        
    #return final filter

    return filtered
