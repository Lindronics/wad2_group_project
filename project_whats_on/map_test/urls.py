from django.conf.urls import url

from map_test import views


urlpatterns = [
    url(r"^$", views.map_test, name="map_test"),
]
