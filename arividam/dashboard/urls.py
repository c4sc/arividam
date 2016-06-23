from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test

from .views import NotificationView, IndexView

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='/')

urlpatterns = [
    url(r'^$', group_required(['Officer'])(IndexView.as_view()), name='index'),
    url(r'^notification/', NotificationView.as_view(), name="notification"),
]
