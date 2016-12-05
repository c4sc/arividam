# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from ajax_select import urls as ajax_select_urls
from arividam.siteconfig.views import RedirectUserView, SiteListView

urlpatterns = [
    #url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    #url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^list-schools/$', SiteListView.as_view(), name='list-schools'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include('arividam.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
    url(r'inbox/notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^dashboard/', include('arividam.dashboard.urls', namespace='dashboard')),
    url(r'^redirect/', RedirectUserView.as_view()),
    url(r'^filer/', include('filer.urls')),
#    url(r'^notifications/', include('arividam.notifications.urls', namespace='notifications')),

    # Your stuff: custom urls includes go here

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

#CMS catch-all patterns should be at the last
urlpatterns = urlpatterns + [ 
    url(r'^', include('cms.urls')),
        ]
