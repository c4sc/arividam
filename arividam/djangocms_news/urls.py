from django.conf.urls import url
from .views import ArticleList, ArticleDetail

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)/$',
        ArticleDetail.as_view(), name='article-detail'),
    # These support permalinks with <article_slug>
    url(r'^(?P<slug>\w[-\w]*)/$',
        ArticleDetail.as_view(), name='article-detail'),
    url(r'^(?P<year>\d{4})/(?P<slug>\w[-\w]*)/$',
        ArticleDetail.as_view(), name='article-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>\w[-\w]*)/$',
        ArticleDetail.as_view(), name='article-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$',  # flake8: NOQA
        ArticleDetail.as_view(), name='article-detail'),

]
