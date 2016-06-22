from django.conf.urls import url
from django.views.generic import TemplateView

from .views import NotificationView, IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^notification/', NotificationView.as_view(), name="notification"),
]
