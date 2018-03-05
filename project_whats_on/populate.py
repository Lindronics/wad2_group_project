# Populate local database with sample data
from datetime import datetime
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project_whats_on.settings")

import django
django.setup()

from whats_on_dot_com.models import *
from django.contrib.auth.models import User

def populate():

    # Load sample data from files
    with open("population_sample_data/category.json", "r") as f:
        categories = json.loads("".join(f.readlines()))
    with open("population_sample_data/tag.json", "r") as f:
        tags = json.loads("".join(f.readlines()))
    with open("population_sample_data/user.json", "r") as f:
        users = json.loads("".join(f.readlines()))
    with open("population_sample_data/event.json", "r") as f:
        events = json.loads("".join(f.readlines()))

    # Populate database with data
    for c in categories:
        add_category(c)
    for t in tags:
        add_tag(t)
    for u in users:
        add_user(u)
    for e in events:
        add_event(e)


def add_category(category):
    c = Category.objects.get_or_create(name=category["name"])[0]
    print("Category added: %s" % c.name)

def add_tag(tag):
    t = Tag.objects.get_or_create(name=tag["name"])[0]
    print("Tag added: %s" % t.name)

def add_user(user):
    u = User.objects.get(username=user["username"])
    if u:
        print("Existing user deleted: %s" % u)
        u.delete()
    u = User.objects.create_user(user["username"], user["email"], user["password"])
    p = UserProfile.objects.get_or_create(user=u)[0]
    p.description = user["description"]
    p.save()
    print("User added: %s" % u.username)

def add_event(event):
    time = datetime.now()
    e = Event.objects.get_or_create(name=event["name"], date_time=time, category=Category.objects.get(name=event["category"]), slug=slugify(event["name"]) + str(time))[0]
    e.description = event["description"]
    e.address = event["address"]
    for host in event["hosts"]: 
        e.host.add(UserProfile.objects.get(user__username=host["username"]))
    for tag in event["tags"]:
        e.tags.add(Tag.objects.get(name=tag["name"]))
    e.save()
    print("Event added: %s" % e.name)


if __name__ == "__main__":
    print("Starting population script for WhatsOnDotCom...")
    populate()