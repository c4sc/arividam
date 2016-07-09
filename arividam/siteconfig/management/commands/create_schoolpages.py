 #!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.db import transaction
from django.conf import settings
from cms.models import Page
from cms.api import create_page, add_plugin
from cms.constants import PAGE_TYPES_ID

class Command(BaseCommand):
    help = 'Creates a school Site'

    def add_arguments(self, parser):
        parser.add_argument('site_id', help='School Site ID to add pages for')

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            site = Site.objects.get(pk=options['site_id'])
        except Site.DoesNotExist:
            raise CommandError("Site with id: {} does not exist".format(options['site_id']))

        default_site = Site.objects.get(pk=settings.SITE_ID)        
        try:
            # get Pages Type root for the default site
            type_root = Page.objects.get(publisher_is_draft=True, 
                            reverse_id=PAGE_TYPES_ID,
                            site=default_site)
        except Page.DoesNotExist:
            raise CommandError("Page Type: School Home not configured")

        types_id = type_root.get_descendants().values_list('pk', flat=True)
        try:
            school_home_type = Page.objects.get(title_set__slug='school-home', pk__in=types_id)
        except Page.DoesNotExist:
            raise CommandError("Page Type: School Home not configured")

        school_home = create_page('Home', 'cms/page.html', settings.LANGUAGE_CODE, slug='home', site=site)
        school_home_type._copy_attributes(school_home, clean=True)
        school_home_type._copy_contents(school_home, settings.LANGUAGE_CODE)
        # copying above attributes switches the site so set it again here
        school_home.site = site
        school_home.publish(settings.LANGUAGE_CODE)
        school_home.save()

        history = create_page(u"ചരിതം", "cms/page.html", settings.LANGUAGE_CODE, slug='history', site=site, in_navigation=True, menu_title=u"ചരിതം", )
        ph_h = history.placeholders.get(slot='content')
        tp_h = add_plugin(ph_h, 'TextPlugin', 'en', body='History of the school')
        history.publish(settings.LANGUAGE_CODE)
        history.save()

        activities = create_page(u"പ്രവർത്തനങ്ങൾ", "cms/page.html", settings.LANGUAGE_CODE, slug="activities", site=site, in_navigation=True, menu_title=u"പ്രവർത്തനങ്ങൾ")
        ph_a = activities.placeholders.get(slot='content')
        tp_a = add_plugin(ph_a, 'TextPlugin', 'en', body='<h1>Activities</h1>')
        activities.publish(settings.LANGUAGE_CODE)
        activities.save()

        teachers = create_page(u"അധ്യാപകരുടെ", "cms/page.html", settings.LANGUAGE_CODE, slug='teachers', site=site, in_navigation=True, menu_title=u"അധ്യാപകരുടെ", )
        ph_t = teachers.placeholders.get(slot='content')
        tp_t = add_plugin(ph_t, 'TextPlugin', 'en', body='<h1>Teachers</h1>List of teachers')
        teachers.publish(settings.LANGUAGE_CODE)
        teachers.save()

        gallery = create_page(u"ചിതമണ്ഡപം", "cms/page.html", settings.LANGUAGE_CODE, slug="gallery", site=site, in_navigation=True, menu_title=u"ചിതമണ്ഡപം", )
        ph_g = gallery.placeholders.get(slot='content')
        tp_g = add_plugin(ph_g, 'TextPlugin', 'en', body='<h1>Gallery</h1>School images')
        gallery.publish(settings.LANGUAGE_CODE)
        gallery.save()

        self.stdout.write("Successfully created school pages", self.style.SUCCESS)

