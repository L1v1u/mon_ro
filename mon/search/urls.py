from django.urls import path, include
from . import views

urlpatterns = [
      path('mester/romania', views.search, name='all_traders_country'),
      path('loc-autocomplete', views.LocAutocomplete.as_view(), name='autocomplete_locs'),
      path('tradertype-autocomplete', views.TraderTypeAutocomplete.as_view(), name='autocomplete_tradertype'),
      path('<trader_type>', views.search, name='trader_search'),
      path('<trader_type>/<county>', views.search, name='trader_country_search'),
      path('<trader_type>/<county>/<loc>', views.search, name='trader_country_loc_search'),
      path('<trader_type>/<trader_type2>/<county>/<loc>', views.search, name='trader_type_country_loc_search'),


]
