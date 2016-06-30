
from cms.models import Page
from django.conf import settings

def get_page_by_slug(slug):
    try:
        return Page.objects.get(
                    title_set__slug=slug,
                    title_set__published=True,
                    title_set__publisher_is_draft=False,
                    site__id=settings.SITE_ID)
    except Page.DoesNotExist:
        return None
