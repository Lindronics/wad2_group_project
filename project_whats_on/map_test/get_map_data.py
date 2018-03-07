import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project_whats_on.settings")

import django
django.setup()

from whats_on_dot_com.models import *

#What I want to do in SQL
#SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) )
#* cos( radians( lng ) - radians(-122) ) + sin( radians(37) )
#* sin( radians( lat ) ) ) )
#AS distance FROM markers HAVING distance < 25 ORDER BY distance;

def extract_query():
    #Using raw sql here as is easier than trying to convert
    #ideally convert as raw sql is somewhat more vulnerable
    #see here for details https://docs.djangoproject.com/en/2.0/topics/db/sql/
    query = Events.objects.raw('SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians(-122) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM markers HAVING distance < 25 ORDER BY distance')

    #test
    print query

extract_query()
