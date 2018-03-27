from django.conf.urls import url, include

from whats_on_dot_com import views


urlpatterns = [
    url(r"^events/$", views.events, name="events"),
    url(r"^events/query/(?P<query>[\w\ ]+)$", views.events, name="events"),
    url(r"^events/add$", views.add_event, name="add_event"),
    url(r"^events/details/(?P<event_pk>[\w\-]+)$", views.event_page, name="event_page"),
    url(r"^events/details/(?P<event_pk>[\w\-]+)/interested$", views.interested, name="interested"),
    url(r"^about$", views.about, name="about"),
    url(r"^profiles$", views.profiles, name="profiles"),
    url(r"^profiles/details/(?P<username>[\w\-]+)$", views.profile, name="profile"),
    url(r"^profiles/details/(?P<username>[\w\-]+)/follow$", views.follow, name="follow"),
    url(r"^profiles/setup$", views.profile_setup, name="profile_setup"),
    url(r"^map$", views.events_map, name="events_map"),
	url(r"^map_test/$", views.map_test, name="map_test"), #delete when main map works
    url(r"^$", views.index, name="index"),  # Provide a redirect to the events page: <hostname>/ maps to <hostname>/events
]
