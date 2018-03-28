# TODO Some things might be broken for now and loads of stuff is missing. 
# Will wait for the corresponding pages and views to make some progress
# and then finish this.

from django import forms
from whats_on_dot_com.models import UserProfile, Category, Tag, Event
from django.contrib.auth.models import User

from registration.forms import RegistrationForm

# Iain's import to get lat lng from adress string
import requests

# Used for creating a new event
class NewEventForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the name of your event.", required=True)
    description = forms.CharField(max_length=1024, help_text="Please enter a description for your event.", required=True)
    date_time = forms.DateTimeField(required=True)
    address = forms.CharField(max_length=128, help_text="Address", required=True)
    location_info = forms.CharField(max_length=128, help_text="Additional location information")
    event_picture = forms.ImageField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    new_tags = forms.CharField(max_length=1024, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    def clean(self):
        cleaned_data = super(NewEventForm,self).clean()
        date_time = cleaned_data.get('date_time')
                
        # Iain's code to get the lat long from the address string
        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
        # Parameters fro gmaps api request
        params = {
        'address': cleaned_data.get('address'),
        'sensor': 'false',
        'key': 'AIzaSyAzbpDPFJ4xudZnqIsjLH3ltL9og-Sihsk',
        }
        # Do the request and get the response
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
                
        result = res['results'][0]
                
        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']
        
        latitude = geodata["lat"]
        longitude = geodata["lng"]
        
        self.address = cleaned_data.get('address')

        return(self.cleaned_data)

    def getlatandlong(self):
        address = self.address
                
        # Iain's code to get the lat long from the address string
        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
        # Parameters fro gmaps api request
        params = {
        'address': address,
        'sensor': 'false',
        'key': 'AIzaSyAzbpDPFJ4xudZnqIsjLH3ltL9og-Sihsk',
        }
        # Do the request and get the response
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        if len(res['results']) ==0:
            return([])
        else:
            result = res['results'][0]
        
                
        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']
        
        latitude = geodata["lat"]
        longitude = geodata["lng"]
        latandlong = [latitude,longitude]

        return(latandlong)

    def clean_date_time(self):
        from django.utils import timezone
        cleaned_data = super(NewEventForm,self).clean()
        date_time = cleaned_data.get('date_time')
        
        if date_time<timezone.now():
            raise forms.ValidationError("please enter a date not in the past")
        else:
            pass
        
        return date_time

    class Meta:
        model = Event
        exclude = ('number_followers', 'host', 'interested',)

# Used for filtering Events on home page
class FilterEventsForm(forms.ModelForm):
    radius_choices = (
        (1, "1 km"),
        (3, "3 km"),
        (5, "5 km"),
        (10, "10 km"),
        (50, "50 km"),
        (999999999999999999999999, "infinite"),
    )
    people_choices = (
        (1, "Friends"),
        (2, "Everyone"),
    )
    date_choices = (
        (1, "Today"),
        (2, "This week"),
        (3, "This month"),
        (4, "This year"),
    )
    name = forms.CharField(max_length=128, required=False)
    search = forms.CharField(max_length=128, required=False)
    search_location = forms.CharField(max_length=128, required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    radius = forms.ChoiceField(choices=radius_choices, required=False, widget=forms.RadioSelect)
    people = forms.ChoiceField(choices=people_choices, initial=2, required=False, widget=forms.RadioSelect)
    date = forms.ChoiceField(choices=date_choices, initial=4, required=False, widget=forms.RadioSelect)

    class Meta:
        model = Event
        fields = ("name",)

# Filter profiles in profiles list view
class FilterProfilesForm(forms.ModelForm):
    people_choices = (
        (1, "Friends"),
        (2, "Everyone"),
    )

    user = forms.CharField(max_length=128, required=False)
    search = forms.CharField(max_length=128, required=False)
    people = forms.ChoiceField(choices=people_choices, required=False, initial=2, widget=forms.RadioSelect)

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

# Register new account (extends django registration redux)
class UserProfileRegistrationForm(RegistrationForm):
    forename = forms.CharField()
    surname = forms.CharField()
    description = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)
