from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site

from .models import GoogleCalendar

# Register your models here.
class CalendarInline(admin.StackedInline):
    fields = ('title', 'calendar_id', 'colour',)
    model = GoogleCalendar
    can_delete = True
    extra = 0

class SiteCalendarAdmin(SiteAdmin):
    inlines = (CalendarInline,)

admin.site.unregister(Site)
admin.site.register(Site, SiteCalendarAdmin)
