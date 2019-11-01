from django.shortcuts import render
from django.http import HttpResponse
from dal import autocomplete
from projects.models import Loc
from traders.models import TraderType

def search(request, trader_type=None, trader_type2= None,county= None,
    loc=None):

    return_str = "{}- {} - {} - {}".format(trader_type,trader_type2,county,loc)
    return HttpResponse(return_str)


def index(request):
    return render(request, 'home.html')


class LocAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return item.loc_name+ ' ('+item.county.county_name+')'

    def get_selected_result_label(self, item):
        return item.loc_name+ ' ('+item.county.county_name+')'

    def get_queryset(self):
        qs = Loc.objects.all().order_by('loc_name')
        if self.q:
            qs = qs.filter(loc_name__unaccent__istartswith=self.q)
        return qs


class TraderTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return item.name

    def get_selected_result_label(self, item):
        return item.name

    def get_queryset(self):
        qs = TraderType.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__unaccent__istartswith=self.q)
        return qs

