from django.shortcuts import render
from django.conf import settings
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from .forms import CreateNotificationForm

from postman.models import Message
from cms.models import Page
from cms.api import create_page, add_plugin

import logging

logger = logging.getLogger(__name__)

# Create your views here.

class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['messages'] = Message.objects.inbox(self.request.user)
        try:
            context['news'] = Page.objects.search("news")[0]
        except IndexError:
            news = create_page('News', 'cms/news.html', settings.LANGUAGE_CODE, reverse_id='news', published=True)
        return context

class NotificationView(FormView):
    template_name = 'dashboard/notification.html'
    form_class = CreateNotificationForm

    def form_valid(self, form):
        logger.debug("form is valid")
        form.post_notification(self.request.user)
        return super(NotificationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard:index')
