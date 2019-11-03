from django.shortcuts import render
from django.http import HttpResponse
from dal import autocomplete
from projects.models import Loc
from traders.models import TraderType, Tradesman
from django.urls import resolve
from django.core.paginator import Paginator

def search(request, trader_type=None, trader_type2=None, county=None, loc=None):

    current_url = resolve(request.path_info).url_name

    if current_url =='all_traders_country':
        tradesman_list = Tradesman.approved_objects.all()
        paginator = Paginator(tradesman_list, 25)  # Show 25 contacts per page
        page = request.GET.get('page')
        tradsmen = paginator.get_page(page)

    # return_str = "{}- {} - {} - {}".format(trader_type,trader_type2,county,loc)
    return render(request, 'list_tradsmen.html', {'tradsmen': tradsmen})


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

