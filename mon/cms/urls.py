from django.urls import path, include
from . import views
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
      path('<url_key>', cache_page(CACHE_TTL)(views.CmsDetailView.as_view()), name='post_detail'),
]
