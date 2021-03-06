from django.conf.urls import url
from django.views.generic import TemplateView
from .views import NotificationView, IndexView
from .decorators import group_required

urlpatterns = [
    url(r'^$', group_required(('Officer',))(IndexView.as_view()), name='index'),
    url(r'^notification/', NotificationView.as_view(), name="notification"),
]
