from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

class SiteMiddleware(object):
    def process_request(self, request):
        host = request.get_host()
        if request.is_secure():
            proto = "https"
        else:
            proto = "http"

        current_site = None
        try:
            current_site = Site.objects.get(domain=request.get_host())
        except Site.DoesNotExist:
            if request.get_host().find(":") >= 0:
                port = ":%s" % request.get_host().split(":")[1]
                try:
                    current_site = Site.objects.get(domain=request.get_host().split(":")[0])
                except Site.DoesNotExist:
                    pass
            else:
                port = ""

            if not current_site:
                current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)
                return HttpResponseRedirect("%s://%s%s%s" % (proto, current_site.domain, port, request.get_full_path()))

        request.current_site = current_site

        settings.SITE_ID = current_site.id
        settings.SITE_NAME = current_site.name

