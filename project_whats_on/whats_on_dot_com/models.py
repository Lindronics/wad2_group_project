from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# USER PROFILE:
# Contains profile information, is linked to django User model
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=1024, blank=True, null=True)

    # Foreign keys
    follows = models.ManyToManyField("this", blank=True)

    def __str__(self):
        return self.user

# CATEGORY:
# Event category
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

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
    slug = models.SlugField(unique=True)
    location_info = models.CharField(max_length=128)

    # perhaps it makes more sense to split the address into different fields?
    address = models.CharField(max_length=1024)

    # Foreign keys
    hosts = models.ManyToManyField(UserProfile)
    interested = models.ManyToManyField(UserProfile)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

