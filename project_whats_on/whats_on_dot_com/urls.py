from django.conf.urls import url, include

from whats_on_dot_com import views


urlpatterns = [
    url(r"^event/add$", views.add_event, name="add_event"),
    url(r"^profiles$", views.profiles, name="profiles"),
    url(r"^events$", views.events, name="events"),
    url(r"^$", views.index, name="index"),  # Provide a redirect to the events page: <hostname>/ maps to <hostname>/events
]