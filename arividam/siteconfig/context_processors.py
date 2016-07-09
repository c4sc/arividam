from django.conf import settings
from django.contrib.sites.models import Site

def default_site(request):
    site = Site.objects.get(pk=settings.DEFAULT_SITE_ID)
    return {
            'DEFAULT_SITE_ID': settings.DEFAULT_SITE_ID,
            'DEFAULT_SITE_URL': site.domain}
