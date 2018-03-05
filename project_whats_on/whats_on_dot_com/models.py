from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# USER PROFILE:
# Contains profile information, is linked to django User model
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    forename = models.CharField(max_length=128, blank=True, null=True)
    surname = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)

    # Foreign keys
    follows = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.user.username

# CATEGORY:
# Event category
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# TAG:
# Tags for events
class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

# EVENT:
# Hosted event
class Event(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, blank=True, null=True)
    date_time = models.DateTimeField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    location_info = models.CharField(max_length=128)
    event_picture = models.ImageField(upload_to="event_images", blank=True)

    # perhaps it makes more sense to split the address into different fields?
    address = models.CharField(max_length=1024)

    # Foreign keys
    host = models.ManyToManyField(UserProfile, related_name="host")
    interested = models.ManyToManyField(UserProfile, related_name="interested", blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

