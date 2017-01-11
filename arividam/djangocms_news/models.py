from __future__ import unicode_literals

from django.db import models
from cms.models import Page

# Create your models here.
class PromotedNews(models.Model):
    page = models.ForeignKey(Page)

