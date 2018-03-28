from registration.backends.simple.views import RegistrationView
from whats_on_dot_com.forms import UserProfileRegistrationForm
from whats_on_dot_com.models import UserProfile

# Extends django registration redux to allow registration in one step

class MyRegistrationView(RegistrationView):
    form_class = UserProfileRegistrationForm

    # If login successful, redirect user to home page
    def get_success_url(self, user): 
            return "/"

    def register(self, form_class):
        new_user = super(MyRegistrationView, self).register(form_class)
        user_profile = UserProfile()
        user_profile.user = new_user
        user_profile.forename = form_class.cleaned_data['forename']
        user_profile.surname = form_class.cleaned_data['surname']
        user_profile.description = form_class.cleaned_data['description']
        user_profile.profile_picture = form_class.cleaned_data['profile_picture']
        user_profile.save()
        return new_user