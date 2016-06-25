from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from postman.models import Message
from postman.api import pm_write, pm_broadcast
from cms.api import create_page, add_plugin
from cms.models import Page

from arividam.siteconfig import models

import logging

logger = logging.getLogger(__name__)

NOTIFICATION_TYPES = [
    ('public', 'Public'),
    ('private', 'Private'),
]

RECIPIENTS = [
    ('dde', 'DDE'),
    ('diet', 'DIET'),
    ('deo', 'DEO'),
    ('ssa', 'SSA'),
    ('it@school','IT@SCHOOL'),
    ('aeo1', 'AEO1'),
    ('aeo2', 'AEO2'),
    ('aeo3', 'AEO3'),
    ('dchss', 'DCHSS'),
    ('dcvhse', 'DCVHSE'),
    ('schools', 'Schools'),
]

SCHOOLS = [
    ('HS', (
        ('hs-govt', 'Govt.'),
        ('hs-aided', 'Aided'),
        ('hs-unaided', 'Unaided'),
        )
    ),
    ('HSS', (
        ('hss-govt', 'Govt.'),
        ('hss-aided', 'Aided'),
        ('hss-unaided', 'Unaided'),
        )
    ),
    ('VHSE', (
        ('vhse-govt', 'Govt.'),
        ('vhse-aided', 'Aided'),
        ('vhse-unaided', 'Unaided'),
        )
    ),
]

class CreateNotificationForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea(), required=True)
    notification_type = forms.ChoiceField(initial='public', choices=NOTIFICATION_TYPES, widget=forms.RadioSelect())
    recipients = forms.ChoiceField(choices=RECIPIENTS, required=False)
    schools = forms.ChoiceField(choices=SCHOOLS, required=False)

    def post_notification(self, user):
        if self.cleaned_data['notification_type'] == 'public':
            # create public notification
            logger.debug("Creating public notification")
            search_result = Page.objects.search("notifications")
            if len(search_result) > 0:
                notifications = search_result[0]
            else:
                #create Notification page
                notifications = create_page("Notifications", "cms/notifications.html", settings.LANGUAGE_CODE, reverse_id='notifications', published=True)
            notification = create_page(self.cleaned_data['title'], 'cms/notification.html', settings.LANGUAGE_CODE, parent=notifications, published=True)
            placeholder = notification.placeholders.get(slot='content')
            add_plugin(placeholder, 'TextPlugin', 'en', 
                body=self.cleaned_data['content'])
        else:
            logger.debug("Creating private notification")
            User = get_user_model()
            if self.cleaned_data['recipients'] != 'schools':
                recipients = [User.objects.get(username=self.cleaned_data['recipients'])]
            else:
                logger.debug("selected school: %s" % self.cleaned_data['schools'])
                schools = models.SiteConfiguration.objects.filter(school_type=self.cleaned_data['schools'])
                recipients = list(User.objects.filter(globalpagepermission__sites__in=[s.site for s in schools]))
                
            # send private notification
            if recipients:
                pm_broadcast(sender=get_user_model().objects.get(username='admin'), 
                        recipients=recipients, 
                        subject=self.cleaned_data['title'], 
                        body=self.cleaned_data['content'])

