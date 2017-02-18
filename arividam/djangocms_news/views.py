from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
from cms.models import Page
from cms.api import create_page
from postman.api import pm_write
from .models import PromotedNews
import json
from arividam.utils import get_default_site_page_by_slug
from django.contrib.auth import get_user_model
import logging
from django.db import IntegrityError
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from aldryn_apphooks_config.mixins import AppConfigMixin
from parler.views import TranslatableSlugMixin, ViewUrlMixin

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
    current_site = get_current_site(request)
    try:
        p = PromotedNews.objects.create(page=page, site=current_site)
    except IntegrityError:
        # article has already been promoted
        return HttpResponse(json.dumps({"promoted": False}), content_type="application/json")
    news = get_default_site_page_by_slug("news")
    current_school = current_site.domain.split(".")[0]
    site = Site.objects.get(pk=settings.DEFAULT_SITE_ID)
    if site != current_site:
        article = create_page("{}-{}".format(current_school, page.get_title(settings.LANGUAGE_CODE)), 'cms/article.html', settings.LANGUAGE_CODE,
                parent=news, published=False, slug=page.get_slug(settings.LANGUAGE_CODE), site=site)
        ph = article.placeholders.get(slot="content")
        old_ph = page.placeholders.get(slot="content")
        plugin = old_ph.get_plugins("en")[0]
        pc = {}
        plugin.copy_plugin(ph, settings.LANGUAGE_CODE, pc, no_signals=False)
        article.publish(settings.LANGUAGE_CODE)
        admin = User.objects.get(username="admin")
        try:
            editor = User.objects.get(username="editor")
            pm_write(sender=admin, recipient=editor, subject="Promoted news", body="A news article has been promoted. You can visit the article at http://www.arividam.in{}?edit&language=en".format(article.get_absolute_url(settings.LANGUAGE_CODE)))
        except User.DoesNotExist:
            pass
    #article.publish(settings.LANGUAGE_CODE)
    return HttpResponse(json.dumps({"promoted": True}), content_type="application/json")

class TemplatePrefixMixin(object):

    def prefix_template_names(self, template_names):
        if (hasattr(self.config, 'template_prefix') and
                self.config.template_prefix):
            prefix = self.config.template_prefix
            return [
                add_prefix_to_path(template, prefix)
                for template in template_names]
        return template_names

    def get_template_names(self):
        template_names = super(TemplatePrefixMixin, self).get_template_names()
        return self.prefix_template_names(template_names)


class EditModeMixin(object):
    """
    A mixin which sets the property 'edit_mode' with the truth value for
    whether a user is logged-into the CMS and is in edit-mode.
    """
    edit_mode = False

    def dispatch(self, request, *args, **kwargs):
        self.edit_mode = (
            self.request.toolbar and self.request.toolbar.edit_mode)
        return super(EditModeMixin, self).dispatch(request, *args, **kwargs)


class PreviewModeMixin(EditModeMixin):
    """
    If content editor is logged-in, show all articles. Otherwise, only the
    published articles should be returned.
    """
    def get_queryset(self):
        qs = super(PreviewModeMixin, self).get_queryset()
        # check if user can see unpublished items. this will allow to switch
        # to edit mode instead of 404 on article detail page. CMS handles the
        # permissions.
        user = self.request.user
        user_can_edit = user.is_staff or user.is_superuser
        if not (self.edit_mode or user_can_edit):
            qs = qs.published()
        #qs = qs.active_translations('en').namespace(self.namespace)
        return qs

class AppHookCheckMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.valid_languages = ['en']
        return super(AppHookCheckMixin, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        # filter available objects to contain only resolvable for current
        # language. IMPORTANT: after .translated - we cannot use .filter
        # on translated fields (parler/django limitation).
        # if your mixin contains filtering after super call - please place it
        # after this mixin.
        qs = super(AppHookCheckMixin, self).get_queryset()
        return qs.translated(*self.valid_languages)



class ArticleDetail(AppConfigMixin, AppHookCheckMixin, PreviewModeMixin,
                    TranslatableSlugMixin, TemplatePrefixMixin, DetailView):
#    model = Article
    slug_field = 'slug'
    year_url_kwarg = 'year'
    month_url_kwarg = 'month'
    day_url_kwarg = 'day'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        """
        This handles non-permalinked URLs according to preferences as set in
        NewsBlogConfig.
        """
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        #set_language_changer(request, self.object.get_absolute_url)
        url = self.object.get_absolute_url()
        if (self.config.non_permalink_handling == 200 or request.path == url):
            # Continue as normal
            return super(ArticleDetail, self).get(request, *args, **kwargs)

        # Check to see if the URL path matches the correct absolute_url of
        # the found object
        if self.config.non_permalink_handling == 302:
            return HttpResponseRedirect(url)
        elif self.config.non_permalink_handling == 301:
            return HttpResponsePermanentRedirect(url)
        else:
            raise Http404('This is not the canonical uri of this object.')

    def get_object(self, queryset=None):
        """
        Supports ALL of the types of permalinks that we've defined in urls.py.
        However, it does require that either the id and the slug is available
        and unique.
        """
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        pk = self.kwargs.get(self.pk_url_kwarg, None)

        if pk is not None:
            # Let the DetailView itself handle this one
            return DetailView.get_object(self, queryset=queryset)
        elif slug is not None:
            # Let the TranslatedSlugMixin take over
            return super(ArticleDetail, self).get_object(queryset=queryset)

        raise AttributeError('ArticleDetail view must be called with either '
                             'an object pk or a slug')

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['prev_article'] = self.get_prev_object(
            self.queryset, self.object)
        context['next_article'] = self.get_next_object(
            self.queryset, self.object)
        return context

    def get_prev_object(self, queryset=None, object=None):
        if queryset is None:
            queryset = self.get_queryset()
        if object is None:
            object = self.get_object(self)
        prev_objs = queryset.filter(
            publishing_date__lt=object.publishing_date
        ).order_by(
            '-publishing_date'
        )[:1]
        if prev_objs:
            return prev_objs[0]
        else:
            return None

    def get_next_object(self, queryset=None, object=None):
        if queryset is None:
            queryset = self.get_queryset()
        if object is None:
            object = self.get_object(self)
        next_objs = queryset.filter(
            publishing_date__gt=object.publishing_date
        ).order_by(
            'publishing_date'
        )[:1]
        if next_objs:
            return next_objs[0]
        else:
            return None


class ArticleListBase(AppConfigMixin, AppHookCheckMixin, TemplatePrefixMixin,
                      PreviewModeMixin, ViewUrlMixin, ListView):
#    model = Article
    show_header = False

    def get_paginate_by(self, queryset):
        if self.paginate_by is not None:
            return self.paginate_by
        else:
            try:
                return self.config.paginate_by
            except AttributeError:
                return 10  # sensible failsafe

    def get_pagination_options(self):
        # Django does not handle negative numbers well
        # when using variables.
        # So we perform the conversion here.
        if self.config:
            options = {
                'pages_start': self.config.pagination_pages_start,
                'pages_visible': self.config.pagination_pages_visible,
            }
        else:
            options = {
                'pages_start': 10,
                'pages_visible': 4,
            }

        pages_visible_negative = -options['pages_visible']
        options['pages_visible_negative'] = pages_visible_negative
        options['pages_visible_total'] = options['pages_visible'] + 1
        options['pages_visible_total_negative'] = pages_visible_negative - 1
        return options

    def get_context_data(self, **kwargs):
        context = super(ArticleListBase, self).get_context_data(**kwargs)
        context['pagination'] = self.get_pagination_options()
        return context


class ArticleList(ArticleListBase):
    """A complete list of articles."""
    show_header = True

    def get_queryset(self):
        qs = super(ArticleList, self).get_queryset()
        # exclude featured articles from queryset, to allow featured article
        # plugin on the list view page without duplicate entries in page qs.
        exclude_count = self.config.exclude_featured
        if exclude_count:
            featured_qs = Article.objects.all().filter(is_featured=True)
            if not self.edit_mode:
                featured_qs = featured_qs.published()
            exclude_featured = featured_qs[:exclude_count].values_list('pk')
            qs = qs.exclude(pk__in=exclude_featured)
        return qs


