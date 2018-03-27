from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.urlresolvers import reverse

#iain funky shit
import math

#import my script from main document tree
#from get_events_in_radius import nearby_locations

from whats_on_dot_com.models import User, UserProfile, Event, Category, Tag
from whats_on_dot_com.forms import NewEventForm, ProfileSetupForm, FilterEventsForm, FilterProfilesForm

# INDEX (home page, redirects to events page)
def index(request):
    return HttpResponseRedirect(reverse('events'))  # Via events url pattern

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
                events, sb = search_bar(events, data["search"])

            # Filter categories
            if data["category"]:
                events_buffer = events
                events = []
                for c in data["category"]:
                    events += events_buffer.filter(category=c)

            # Filter people
            if data["people"]:
                p = int(data["people"])
                if p == 1:
                    up = UserProfile.objects.get(user__username=request.user.username)
                    user_profiles = UserProfile.objects.all().filter(follows=up)
                    events = events.filter(host__in=user_profiles)
        else:
            print(filter_events_form.errors)

    # If GET, check if arguments were passed into the search bar
    else:
        if query:
            events, sb = search_bar(events, query)

    # Sort events by popularity
    try:
        events = events.order_by('-number_followers')
    except:
        pass

    context_dict = {
        "events":events, 
        "categories":categories, 
        "filter_events_form":filter_events_form, 
        "search_bar_initial":sb
    }

    if UserProfile.objects.filter(user__username=request.user).exists():
        context_dict["profile"] = UserProfile.objects.get(user__username=request.user)

    #print(events)
    return render(request, 'whats_on_dot_com/events.html', context_dict)

# EVENTS MAP (map overview of nearby events)
def events_map(request):

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
    return render(request, 'whats_on_dot_com/events_map.html', context_dict)
	
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
    }

    if UserProfile.objects.filter(user__username=request.user).exists():
        context_dict["profile"] = UserProfile.objects.get(user__username=request.user)

    return render(request, "whats_on_dot_com/event_page.html", context_dict)

# ADD EVENT (for adding a new event)
@login_required
def add_event(request):
    form = NewEventForm()

    # Get data from form, add to model if valid
    if request.method == 'POST':
        form = NewEventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save()
            data = form.cleaned_data
            
            #Getting the latitude and longitude
            latandlong = form.getlatandlong()
            event.latitude = latandlong[0]
            event.longitude = latandlong[1]

            # Add new tags
            if data["new_tags"]:
                for raw_tag in data["new_tags"].split(","):
                    tag = raw_tag.strip()
                    t = Tag.objects.get_or_create(name=tag)[0]
                    event.tags.add(t.pk)

            # Add picture
            event.event_picture = data['event_picture']

            # Add host
            up = UserProfile.objects.get(user__username=request.user)
            event.host.add(up)
            event.save()

            return HttpResponseRedirect(reverse('event_page', args=[event.pk]))
        else:
            print(form.errors)

    context_dict = {
        "event_form":form,
    }

    return render(request, 'whats_on_dot_com/add_event.html', context_dict)

# PROFILES (profiles list including search etc.)
@login_required
def profiles(request):
    filter_profiles_form = FilterProfilesForm()

    # Initial value of search bar
    sb = "Search..."

    # Initial queryset
    user_profiles = UserProfile.objects.all()

    # If filter request
    if request.method == "POST":
        filter_profiles_form = FilterProfilesForm(request.POST)

        if filter_profiles_form.is_valid():
            data = filter_profiles_form.cleaned_data

            # Filter people
            if data["people"]:
                p = int(data["people"])
                if p == 1:
                    up = UserProfile.objects.get(user__username=request.user.username)
                    user_profiles = user_profiles.filter(follows=up)

            # Filter search bar
            sb = data["search"]
            if sb:
                # Search for usernames and real names
                splitted = sb.split(" ")
                if len(splitted) > 1:
                    user_profiles = user_profiles.filter(forename__icontains=splitted[0]) | user_profiles.filter(surname__icontains=splitted[1])
                else:
                    user_profiles = user_profiles.filter(user__username__icontains=sb) | user_profiles.filter(forename__icontains=sb) | user_profiles.filter(surname__icontains=sb)

        else:
            print(filter_profiles_form.errors)


    context_dict = {
        "profiles":user_profiles, 
        "search_bar_initial":sb,
        "filter_profiles_form":filter_profiles_form,
    }

    return render(request, 'whats_on_dot_com/profiles.html', context_dict)

# ABOUT (about page with project information)
def about(request):
    return render(request, 'whats_on_dot_com/about.html')

# PROFILE (page for personal profile overview)
@login_required
def profile(request, username):
    try:
        user_profile = UserProfile.objects.get(user__username=username)
        context_dict = {
            "profile":user_profile,
        }
        if request.user:
            context_dict["this_user"] = UserProfile.objects.get(user__username=request.user.username)
        return render(request, 'whats_on_dot_com/profile.html', context_dict)

    except UserProfile.DoesNotExist:
        if username==request.user.username:
            print("SETUP")
            return HttpResponseRedirect(reverse('profile_setup'))
        else:
            print("NO SETUP")
            return HttpResponseRedirect(reverse('events'))

# PROFILE_SETUP (changing profile values such as name, description)
@login_required
def profile_setup(request):
    if request.method == 'POST': 
        profile_setup_form = ProfileSetupForm(request.POST, request.FILES)

        if profile_setup_form.is_valid():

            # Get current user and profile from request
            user = request.user
            profile = UserProfile.objects.get_or_create(user = user)[0]
            data = profile_setup_form.cleaned_data
            
            # Change attributes
            profile.forename = data['forename']
            profile.surname = data['surname']
            profile.description = data['description']
            profile.profile_picture = data['profile_picture']
            profile.save()

            return(HttpResponseRedirect(reverse('profile', args=[request.user])))
        else:
            # Invalid form!
            print(profile_setup_form.errors)
    else:
        # Render form if request not post
        profile_setup_form = ProfileSetupForm()

        context_dict = {
            "profile_setup_form":profile_setup_form,
            }

    return render(request, 'whats_on_dot_com/profile_setup.html', context_dict)

# INTERESTED (for following or unfollowing an event)
@login_required
def interested(request, event_pk):
    up = UserProfile.objects.get(user__username=request.user)
    e = Event.objects.get(pk=event_pk)

    # Toggle following status
    if e.interested.filter(user__username=request.user).exists():
        e.interested.remove(up)
    else:
        e.interested.add(up)

    # Update number of followers
    e.number_followers = e.interested.all().count()
    e.save()

    # Redirect to where user was coming from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# FOLLOW (for following or unfollowing a profile)
@login_required
def follow(request, username):
    up = UserProfile.objects.get(user__username=request.user)
    subject = UserProfile.objects.get(user__username=username)

    # Toggle following status
    if up.follows.filter(user__username=username).exists():
        up.follows.remove(subject)
    else:
        up.follows.add(subject)

    # Update number of followers
    up.save()

    # Redirect to where user was coming from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
