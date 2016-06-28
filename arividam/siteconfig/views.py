from django.shortcuts import render, redirect
from django.views.generic.base import RedirectView
from django.contrib.auth import get_user_model

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

