from django.contrib import admin
from whats_on_dot_com.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "forename", "surname", "description", )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )

class TagAdmin(admin.ModelAdmin):
    list_display = ("name", )

class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "date_time", "number_followers", "location_info", "address")



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
