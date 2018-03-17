"""project_whats_on URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from django.conf import settings 
from django.conf.urls.static import static

# If login successful, redirect user to home page
class MyRegistrationView(RegistrationView): 
    def get_success_url(self, user): 
        return "/whats_on_dot_com/"

urlpatterns = [
    url(r"^admin/", admin.site.urls),
	url(r"^map_test/", include('map_test.urls')),
    url(r"^accounts/", include("registration.backends.simple.urls")),
    url(r"^", include("whats_on_dot_com.urls")),# Match to start of urls used in the whats_on_dot_com app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

