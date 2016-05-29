from django.contrib import admin
from django.contrib.sites.models import Site
from arividam.contrib.djangocms_googlecalendar.admin import SiteCalendarAdmin

from .models import SiteConfiguration

# Register your models here.
class SiteConfigurationInlineAdmin(admin.StackedInline):
    model = SiteConfiguration

class SiteConfigurationAdmin(SiteCalendarAdmin):
    inlines = (SiteConfigurationInlineAdmin,) + SiteCalendarAdmin.inlines 

admin.site.unregister(Site)
admin.site.register(Site, SiteConfigurationAdmin)
