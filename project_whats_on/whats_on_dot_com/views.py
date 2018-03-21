from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

#iain funky shit
import math

#import my script from main document tree
#from get_events_in_radius import nearby_locations

from whats_on_dot_com.models import User, UserProfile, Event, Category
from whats_on_dot_com.forms import NewEventForm, ProfileSetupForm, FilterEventsForm, FilterProfilesForm

# INDEX (home page, redirects to events page)
def index(request):
    return HttpResponseRedirect('events')  # Via events url pattern

# EVENTS (events page with events in grid list)
def events(request, query=""):

    def search_bar(events, search_term):
        events_buffer = events

        # Consider names
        events = events_buffer.filter(name__icontains=search_term)

        # Consider tags and hosts
        for event in events_buffer:
            if event.tags.filter(name=search_term).exists() or event.host.filter(user__username=search_term).exists():
                events = events | events_buffer.filter(pk=event.pk)

        # Consider categories
        events = events | events_buffer.filter(category__name__icontains=search_term)
        return events, search_term 


    filter_events_form = FilterEventsForm()

    # Initial value of search bar
    sb = "Search..."

    # Initial querysets
    events = Event.objects.all()
    categories = Category.objects.all()

    # If filter request
    if request.method == "POST":
        filter_events_form = FilterEventsForm(request.POST)

        if filter_events_form.is_valid():
            data = filter_events_form.cleaned_data

            # If search term provided, filter by search bar
            if data["search"]:
<<<<<<< HEAD
                events, sb = search_bar(events, data["search"])
=======
                events = events.filter(name__icontains=data["search"])
                #sb = data["search"]
>>>>>>> 7a0c56d182d82ff84babccd758c58acbf751f6ad

            # Filter categories
            if data["category"]:
                events_buffer = events
                events = []
                for c in data["category"]:
                    events += events_buffer.filter(category=c)

            # Filter people
            # TODO yields strange results for now, will fix later
            if data["people"]:
                p = int(data["people"])
                queryset = []
                if p == 1:
                    # People I follow
                    queryset = UserProfile.objects.get(user=request.user).follows.all()
                if p == 2:
                    # My followers
                    queryset = UserProfile.objects.all().filter(follows=UserProfile.objects.get(user=request.user))
                if p == 3:
                    # TODO Popular people 
                    pass
                print(queryset)
                if queryset:
                    events_buffer = events
                    events = Event.objects.all().filter(pk=-1)
                    for p in queryset:
                        events = events | events_buffer.filter(interested=p)
        else:
            print(filter_events_form.errors)

    # If GET, check if arguments were passed into the search bar
    else:
        if query:
            events, sb = search_bar(events, query)

    context_dict = {
        "events":events, 
        "categories":categories, 
        "filter_events_form":filter_events_form, 
        "search_bar_initial":sb}

    #print(events)
    return render(request, 'whats_on_dot_com/events.html', context_dict)

# EVENTS MAP (map overview of nearby events)
def events_map(request):
    #COPY PASTING SCRIPT BECAUSE SHIT IS BROKEN AND I WANT IT TO BE NOT

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


    #think this is where I should put fns that I need to call from template
    map_pointz = nearby_locations(55.8, -4.2, 10, 50) #temporary hard code to test. Fix to take data from form
    #print (map_points)
    map_points = ["test"]
    #test
    #test
    return render(request, 'whats_on_dot_com/events_map.html')
	
#delete after main map works
def map_test(request):

    #C+P CODE CAUSE I A SMART BOY

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
	

    #testing
    map_points = nearby_locations(55.8, -4.2, 10, 50)
    #map_points = Event.objects.all()
    #DUMBASS ME DIDNT REMEMBER TO USE CONTEXT DICT
    context_dict = {"map_points": map_points}
    return render(request, 'whats_on_dot_com/map_test.html', context_dict)


# EVENT PAGE (event details page)
def event_page(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    interested = event.interested.all()
    tags = event.tags.all()
    host = event.host.all()
    categories = Category.objects.all()
    print(host)

    context_dict = {
        "event":event, 
        "interested":interested, 
        "tags":tags,
        "host":host,
        "categories":categories,
    }

    return render(request, "whats_on_dot_com/event_page.html", context_dict)

# ADD EVENT (for adding a new event)
@login_required
def add_event(request):
    form = NewEventForm()
    categories = Category.objects.all()

    # Get data from form, add to model if valid
    if request.method == 'POST':
        form = NewEventForm(request.POST)

        if form.is_valid():
            # TODO further code might be necessary to get tags, hosts, category from form
            event = form.save(commit=True)
            #form.save()
            print("Event added: %s" % event.name)
            #return HttpResponseRedirect('/')
            return index(request)
        else:
            print(form.errors)

        context_dict = {
        "categories":categories
        }

    return render(request, 'whats_on_dot_com/add_event.html', {"form":form})

# PROFILES (profiles list including search etc.)
def profiles(request):
    filter_profiles_form = FilterProfilesForm()

    # Initial value of search bar
    sb = "Search..."

    # Initial queryset
    user_profiles = UserProfile.objects.all()

    # If filter request
    if request.method == "POST":
        filter_events_form = FilterEventsForm(request.POST)

        if filter_events_form.is_valid():
            data = filter_events_form.cleaned_data

            # Filter search bar
            sb = data["search"]
            if sb:
                # Search for usernames and real names
                # TODO sort of a hack ATM to search for combined fore- and surnames
                splitted = sb.split(" ")
                if len(splitted) > 1:
                    user_profiles = user_profiles.filter(forename__icontains=splitted[0]) | user_profiles.filter(surname__icontains=splitted[1])
                else:
                    user_profiles = user_profiles.filter(user__username__icontains=sb) | user_profiles.filter(forename__icontains=sb) | user_profiles.filter(surname__icontains=sb)

        else:
            print(filter_profiles_form.errors)


    context_dict = {
        "profiles":user_profiles, 
        "search_bar_initial":sb
    }

    return render(request, 'whats_on_dot_com/profiles.html', context_dict)

# ABOUT (about page with project information)
def about(request):
    return render(request, 'whats_on_dot_com/about.html')

# PROFILE (page for personal profile overview)
@login_required
def profile(request, username):
    user_profile = UserProfile.objects.get(user__username=username)

    context_dict = {
        "profile":user_profile,
        "following":user_profile.follows.all(),
    }
    return render(request, 'whats_on_dot_com/profile.html', context_dict)

# PROFILE_SETUP (changing profile values such as name, description)
@login_required
def profile_setup(request):
    if request.method == 'POST': 
        profile_setup_form = ProfileSetupForm(data=request.POST)

        if profile_setup_form.is_valid():

            # Get current user and profile from request
            user = request.user
            profile = UserProfile.objects.get_or_create(user = user)[0]
            data = profile_setup_form.cleaned_data
            
            # Change attributes
            profile.forename = data['forename']
            profile.surname = data['surname']
            profile.description = data['description']
            if 'picture' in request.FILES:
                print("PICTURE") 
                profile.profile_picture = request.FILES['picture']
            profile.save()
        else:
            # Invalid form!
            print(profile_setup_form.errors)
    else:
        # Render form if request not post
        profile_setup_form = ProfileSetupForm()

    return render(request, 'whats_on_dot_com/profile_setup.html', {"profile_setup_form":profile_setup_form})


