from .models import Cms
from django.utils import timezone
from django.views.generic.detail import DetailView


class CmsDetailView(DetailView):
    """
    This class will load all the cms pages from db
    and display them to a specific route
    """
    model = Cms
    slug_field = 'url_key'
    slug_url_kwarg = 'url_key'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context