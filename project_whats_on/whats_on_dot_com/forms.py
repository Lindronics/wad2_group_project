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
        exclude = ('number_followers', 'latitude', 'longtitude', 'host', 'interested', 'category', 'slug')

# Used for filtering Events on home page
class FilterEventsForm(forms.ModelForm):
    radius_choices = (
        (1, "1 km"),
        (3, "3 km"),
        (5, "5 km"),
        (10, "10 km"),
        (50, "50 km"),
    )
    people_choices = (
        (1, "People I follow"),
        (2, "My followers"),
        (3, "Popular profiles"),
    )
    date_choices = (
        (1, "Today"),
        (2, "This week"),
        (3, "This month"),
        (4, "This year"),
    )
    name = forms.CharField(max_length=128, required=False)
    search = forms.CharField(max_length=128, required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    radius = forms.ChoiceField(choices=radius_choices, required=False, widget=forms.RadioSelect)
    people = forms.ChoiceField(choices=people_choices, required=False, widget=forms.RadioSelect)
    date = forms.ChoiceField(choices=date_choices, required=False, widget=forms.RadioSelect)

    class Meta:
        model = Event
        fields = ("name",)

class FilterProfilesForm(forms.ModelForm):
    people_choices = (
        (1, "People I follow"),
        (2, "My followers"),
        (3, "Popular profiles"),
    )

    user = forms.CharField(max_length=128, required=False)
    search = forms.CharField(max_length=128, required=False)
    people = forms.ChoiceField(choices=people_choices, required=False, widget=forms.RadioSelect)

    class Meta:
        model = UserProfile
        fields = ("user", )

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

