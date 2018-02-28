from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# INDEX
# home page
def index(request):
    return render(request, 'whats_on_dot_com/index.html', {})

def events(request):
    return render(request, 'whats_on_dot_com/index.html', {})

def add_event(request):
    return render(request, 'whats_on_dot_com/index.html', {})

def profiles(request):
    return render(request, 'whats_on_dot_com/index.html', {})
