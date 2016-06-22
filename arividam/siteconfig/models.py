from __future__ import unicode_literals

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

def site_css_path(instance, filename):
    return 'sitecss/{0}/site.css'.format(instance.site.domain)

def banner_path(instance, filename):
    return 'bannerimg/{0}/{1}'.format(instance.site.domain, filename)

ST_HS_GOVT = 'hs-govt'
ST_HS_AIDED = 'hs-aided'
ST_HS_UNAIDED = 'hs-unaided'

ST_HSS_GOVT = 'hss-govt'
ST_HSS_AIDED = 'hss-aided'
ST_HSS_UNAIDED = 'hss-unaided'

ST_VHSE_GOVT = 'vhse-govt'
ST_VHSE_AIDED = 'vhse-aided'
ST_VHSE_UNAIDED = 'vhse-unaided'

SCHOOL_TYPES = (
    (ST_HS_GOVT, 'HS - Govt'),
    (ST_HS_AIDED, 'HS - Aided'),
    (ST_HS_UNAIDED, 'HS - Unaided'),
    (ST_HSS_GOVT, 'HSS - Govt'),
    (ST_HSS_AIDED, 'HSS - Aided'),
    (ST_HSS_UNAIDED, 'HSS - Unaided'),
    (ST_VHSE_GOVT, 'VHSE - Govt'),
    (ST_VHSE_AIDED, 'VHSE - Aided'),
    (ST_VHSE_UNAIDED, 'VHSE - Unaided'),
)

# Create your models here.
class SiteConfiguration(models.Model):
    site = models.OneToOneField(Site, related_name='config', on_delete=models.CASCADE)
    site_css = models.FileField(upload_to=site_css_path, blank=True)
    banner_logo = models.ImageField(upload_to=banner_path, blank=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES, blank=True)
    school_code = models.IntegerField(default=0)
