from __future__ import unicode_literals

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

def site_css_path(instance, filename):
    return 'sitecss/{0}/site.css'.format(instance.site.domain)

def banner_path(instance, filename):
    return 'bannerimg/{0}/{1}'.format(instance.site.domain, filename)

# Create your models here.
class SiteConfiguration(models.Model):
    site = models.OneToOneField(Site, related_name='config', on_delete=models.CASCADE)
    site_css = models.FileField(upload_to=site_css_path)
    banner_logo = models.ImageField(upload_to=banner_path)

