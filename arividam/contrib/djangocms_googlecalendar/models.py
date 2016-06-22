from __future__ import unicode_literals

from django.db import models

from cms.models.pluginmodel import CMSPlugin
from django.contrib.sites.models import Site

class GoogleCalendar(CMSPlugin):
    calendar_id = models.CharField(max_length=128, blank=False)
    site = models.ForeignKey(Site, related_name="googlecalendars")
    title = models.CharField(max_length=32, blank=True)
    colour = models.CharField(max_length=6, blank=True, help_text='Colour in hex format: rrggbb')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

# Create your models here.
