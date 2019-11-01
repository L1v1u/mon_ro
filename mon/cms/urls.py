from django.urls import path, include
from . import views

urlpatterns = [
      path('<url_key>', views.CmsDetailView.as_view(), name='post_detail'),
]
