from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from whats_on_dot_com.models import User, UserProfile, Event, Category
from whats_on_dot_com.forms import NewEventForm, ProfileSetupForm, FilterEventsForm, FilterProfilesForm

# INDEX (home page, redirects to events page)
def index(request):
    return HttpResponseRedirect('events')  # Via events url pattern

# EVENTS (events page with events in grid list)
def events(request):
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
            print(data)

            # Filter search bar
            if data["search"]:
                events = events.filter(name__icontains=data["search"])
                sb = data["search"]

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

    context_dict = {
        "events":events, 
        "categories":categories, 
        "filter_events_form":filter_events_form, 
        "search_bar_initial":sb}

    #print(events)
    return render(request, 'whats_on_dot_com/events.html', context_dict)

# EVENT PAGE (event details page)
def event_page(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    interested = event.interested.all()
    tags = event.tags.all()

    context_dict = {
        "event":event, 
        "interested":interested, 
        "tags":tags
    }
    
    return render(request, "whats_on_dot_com/event_page.html", context_dict)

# ADD EVENT (for adding a new event)
@login_required
def add_event(request):
    form = NewEventForm()

    # Get data from form, add to model if valid
    if request.method == 'POST':
        form = NewEventForm(request.POST)

        if form.is_valid():
            # TODO further code might be necessary to get tags, hosts, category from form
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

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
def profile(request, username):
    user_profile = UserProfile.objects.get(user__username=username)
    return render(request, 'whats_on_dot_com/profile.html', {"profile":user_profile})

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


