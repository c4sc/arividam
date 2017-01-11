from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.sites.models import Site

# Create your views here.
from cms.models import Page
from cms.api import create_page
from postman.api import pm_write
from .models import PromotedNews
import json
from arividam.utils import get_default_site_page_by_slug
from django.contrib.auth import get_user_model
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

def check_promoted(request, page_id):
    page_id = int(page_id)
    page = Page.objects.get(pk=page_id)
    if PromotedNews.objects.filter(page=page).exists():
        data = { "promoted": True }
    else:
        data = { "promoted": False }

    return HttpResponse(json.dumps(data), content_type="application/json")

def promote_news(request, page_id):
    page_id = int(page_id)
    page = Page.objects.get(pk=page_id)
    logger.debug(page)
    p = PromotedNews.objects.create(page=page)
    news = get_default_site_page_by_slug("news")
    site = Site.objects.get(pk=settings.DEFAULT_SITE_ID)
    article = create_page(page.get_title(settings.LANGUAGE_CODE), 'cms/article.html', settings.LANGUAGE_CODE,
            parent=news, published=False, slug=page.get_slug(settings.LANGUAGE_CODE), site=site)
    ph = article.placeholders.get(slot="content")
    old_ph = page.placeholders.get(slot="content")
    plugin = old_ph.get_plugins("en")[0]
    pc = {}
    plugin.copy_plugin(ph, settings.LANGUAGE_CODE, pc, no_signals=False)
    admin = User.object.get(username="admin")
    try:
        editor = User.objects.get(username="editor")
        pm_write(sender=admin, recipient=editor, subject="Promoted news", body="A news article has been promoted. You can visit the article at http://www.arividam.in/{}?edit&language=en".format(article.get_absolute_url(settings.LANGUAGE_CODE)))
    except User.DoesNotExist:
        pass
    #article.publish(settings.LANGUAGE_CODE)
    return HttpResponse(json.dumps({"promoted": True}), content_type="application/json")
