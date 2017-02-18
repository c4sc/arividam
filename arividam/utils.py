
from cms.models import Page
from django.conf import settings

def get_page_by_slug(slug):
    """Returns a cms.Page by slug
    for the current site
    """
    try:
        return Page.objects.get(
                    title_set__slug__startswith=slug,
                    title_set__published=True,
                    title_set__publisher_is_draft=False,
                    site__id=settings.SITE_ID)
    except Page.DoesNotExist:
        return None

def get_default_site_page_by_slug(slug):
    """Returns a cms.Page by slug
    for the default site
    """
    try:
        return Page.objects.get(
                    title_set__slug__startswith=slug,
                    title_set__published=True,
                    title_set__publisher_is_draft=False,
                    site__id=settings.DEFAULT_SITE_ID)
    except Page.DoesNotExist:
        return None

