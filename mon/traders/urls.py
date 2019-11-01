from django.conf.urls import url
from . import views

urlpatterns = [
    url('create', views.TradesmanSaveView.as_view() ,name='create-tradesman')

]