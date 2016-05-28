from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import GoogleCalendar

class GoogleCalendarPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Google Calendar")
    render_template = "djangocms_googlecalendar/plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(GoogleCalendarPlugin, self).render(context, instance, placeholder)
        return context

plugin_pool.register_plugin(GoogleCalendarPlugin)
