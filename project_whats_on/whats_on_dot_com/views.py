from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from whats_on_dot_com.models import User, UserProfile, Event

from whats_on_dot_com.forms import NewEventForm, ProfileSetupForm

# INDEX (home page, redirects to events page)
def index(request):
    return HttpResponseRedirect('events')  # Via events url pattern

# EVENTS (events page with events in grid list)
def events(request):
    events = Event.objects.all()
    return render(request, 'whats_on_dot_com/events.html', {"events":events})

# ADD EVENT (for adding a new event)
@login_required
def add_event(request):
    form = NewEventForm()

    # Get data from form, add to model if valid
    if request.method == 'POST':
        form = NewEventForm(request.POST)

        if form.is_valid():
            # TODO further code might be necessary to get tags, hosts, category from form
            event = form.save(commit=True)
            print("Event added: %s" % event.name)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'whats_on_dot_com/add_event.html', {"form":form})

# PROFILES (profiles list including search etc.)
def profiles(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'whats_on_dot_com/profiles.html', {"profiles":user_profiles})

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


