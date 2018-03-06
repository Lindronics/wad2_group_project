from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# INDEX
# home page
def index(request):
    return HttpResponseRedirect('events')  # Via events url pattern

def events(request):
    return render(request, 'whats_on_dot_com/events.html', {})

def add_event(request):
    return render(request, 'whats_on_dot_com/add_event.html', {})

def profiles(request):
    return render(request, 'whats_on_dot_com/profiles.html', {})

def map_test(request):
    return render(request, '/map_test.html', {})
