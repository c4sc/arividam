from __future__ import unicode_literals

from django.db import models
from cms.models import Page
from djangocms_text_ckeditor.fields import HTMLField
from cms.models.fields import PlaceholderField
from filer.fields.image import FilerImageField
from django.contrib.sites.models import Site

# Create your models here.
class PromotedNews(models.Model):
    page = models.OneToOneField(Page)
    thumbnail = FilerImageField(null=True, blank=True, 
            on_delete=models.SET_NULL)
    extract = HTMLField(verbose_name="extract", default="",
            help_text="A brief description of the article used in the featured lists",
            blank=True)
    site = models.ForeignKey(Site, help_text="The site the article is accessible from", verbose_name="site",
            related_name="djangocms_articles")

#class Article(models.Model):
#    thumbnail = FilerImageField(null=True, blank=True, 
#            on_delete=models.SET_NULL)
#    extract = HTMLField(verbose_name="extract", default="",
#            help_text="A brief description of the article used in the featured lists",
#            blank=True)
#    content = PlaceholderField("article_content", related_name="article_content")
#    site = models.ForeignKey(Site, help_text="The site the article is accessible from", verbose_name="site",
#            related_name="djangocms_articles")
