from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from whats_on_dot_com.forms import NewEventForm

# INDEX (home page, redirects to events page)
def index(request):
    return HttpResponseRedirect('events')  # Via events url pattern

# EVENTS (events page with events in grid list)
def events(request):
    return render(request, 'whats_on_dot_com/events.html', {})

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
    return render(request, 'whats_on_dot_com/profiles.html', {})

# ABOUT (about page with project information)
def about(request):
    return render(request, 'whats_on_dot_com/about.html')


