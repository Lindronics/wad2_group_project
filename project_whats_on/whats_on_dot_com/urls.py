from django.conf.urls import url, include

from whats_on_dot_com import views


urlpatterns = [
    url(r"^event/add$", views.add_event, name="add_event"),
    url(r"^profiles$", views.profiles, name="profiles"),
    url(r"^profiles/(?P<username>[\w\-]+)$", views.profile, name="profile"),
    url(r"^profile/setup$", views.profile_setup, name="profile_setup"),
    url(r"^events$", views.events, name="events"),
    url(r"^map$", views.events_map, name="events_map"),
	url(r"^map_test/$", views.map_test, name="map_test"), #delete when main map works
	url(r"^map_test2/$", views.map_test2, name="map_test2"), #delete when main map works
	url(r"^map_test3/$", views.map_test3, name="map_test3"), #delete when main map works
    url(r"^events/(?P<event_pk>[\w\-]+)$", views.event_page, name="event_page"),
    url(r"^$", views.index, name="index"),  # Provide a redirect to the events page: <hostname>/ maps to <hostname>/events
]
