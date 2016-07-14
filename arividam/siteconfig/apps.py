from __future__ import unicode_literals

from django.apps import AppConfig
from cms.cms_plugins import AliasPlugin
from cms.plugin_pool import plugin_pool


class SiteconfigConfig(AppConfig):
    name = 'siteconfig'
    verbose_name = "Site Configuration"

    def ready(self):
        def return_pass(self, r, p):
            pass
        AliasPlugin.get_extra_global_plugin_menu_items = return_pass
        AliasPlugin.get_extra_placeholder_menu_items = return_pass
        plugin_pool.unregister_plugin(AliasPlugin)

