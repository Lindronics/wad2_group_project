from django.conf.urls import url, include

from whats_on_dot_com import views


urlpatterns = [
    url(r"^event/add$", views.add_event, name="add_event"),
    url(r"^profiles$", views.profiles, name="profiles"),
    url(r"^profiles/(?P<username>[\w\-]+)$", views.profile, name="profile"),
    url(r"^profile/setup$", views.profile_setup, name="profile_setup"),
    url(r"^events/$", views.events, name="events"),
    url(r"^events/(?P<query>[\w\ ]+)$", views.events, name="events"),
    url(r"^map$", views.events_map, name="events_map"),
	url(r"^map_test/$", views.map_test, name="map_test"), #delete when main map works
    url(r"^event_details/(?P<event_pk>[\w\-]+)$", views.event_page, name="event_page"),
    url(r"^event_details/(?P<event_pk>[\w\-]+)/interested$", views.interested, name="interested"),
    url(r"^$", views.index, name="index"),  # Provide a redirect to the events page: <hostname>/ maps to <hostname>/events
]
