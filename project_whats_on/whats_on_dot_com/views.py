from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# INDEX
# home page
def index(request):
    return HttpResponse("test")
