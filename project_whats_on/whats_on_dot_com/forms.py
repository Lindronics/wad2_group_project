# TODO Some things might be broken for now and loads of stuff is missing. 
# Will wait for the corresponding pages and views to make some progress
# and then finish this.

from django import forms
from whats_on_dot_com.models import UserProfile, Category, Tag, Event
from django.contrib.auth.models import User

# Used for creating a new event
class NewEventForm(forms.ModelForm):
    name = forms.CharField(label = 'Event Name', max_length=128, help_text="Please enter the name of your event.")
    description = forms.CharField(label = 'Description', max_length=1024, help_text="Please enter a description for your event.")
    date_time = forms.DateTimeField(label = 'Date Time', )
    address = forms.CharField(label = 'Address', max_length=128, help_text="Address")
    location_info = forms.CharField(label = 'Location Info', max_length=128, help_text="Additional location information")
    event_picture = forms.ImageField(label = 'Picture', )
    
    # TODO implement selecting hosts, category, tags when creating event
    # ideally in a dropdown menu

    class Meta:
        model = Event
        exclude = ()

# Used for filtering Events on home page
class FilterEventsForm(forms.ModelForm):
    search_term = forms.CharField(max_length=128)
    
# Set up profile for registered account
class ProfileSetupForm(forms.ModelForm):
    forename = forms.CharField(max_length=128)
    surname = forms.CharField(max_length=128)
    description = forms.CharField(max_length=1024)

    # TODO picture upload broken atm
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile 
        fields = ("forename", "surname", "description", "profile_picture")