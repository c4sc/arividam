from django.shortcuts import render, redirect
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from arividam.siteconfig.models import SiteConfiguration
from arividam.siteconfig import models
from django.db.models import Q

User = get_user_model()
# Create your views here.

class RedirectUserView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.groups.filter(name__in=['Officer']):
            return '/dashboard/'
        else:
            return '/'

class SiteListView(ListView):
    model = Site
    template_name = 'siteconfig/sitelist.html'

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        context['govt'] = SiteConfiguration.objects.filter(
                Q(school_type=models.ST_HS_GOVT) | 
                Q(school_type=models.ST_HSS_GOVT) |
                Q(school_type=models.ST_VHSE_GOVT))
        context['unaided'] = SiteConfiguration.objects.filter(
                Q(school_type=models.ST_HS_UNAIDED) |
                Q(school_type=models.ST_HSS_UNAIDED) |
                Q(school_type=models.ST_VHSE_UNAIDED))
        context['aided'] = SiteConfiguration.objects.filter(
                Q(school_type=models.ST_HS_AIDED) |
                Q(school_type=models.ST_HSS_AIDED) |
                Q(school_type=models.ST_VHSE_AIDED))
        return context
