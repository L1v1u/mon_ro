from django.shortcuts import render
from django.http import HttpResponse
from dal import autocomplete
from projects.models import Loc
from traders.models import TraderType, Tradesman
from django.urls import resolve
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import json
from traders.models import TraderType
from projects.models import County, Loc

URL_CACHE_TTL = getattr(settings, 'URL_CACHE_TTL', DEFAULT_TIMEOUT)


def get_cache_url(url_path):
    if url_path in cache:
        return cache.get(url_path)
    else:
        json_url_path = json.dumps(get_url(url_path))
        cache.set(url_path, json_url_path, timeout=URL_CACHE_TTL)
        return json_url_path


def get_url(url_path):

    empty_list = {
        'trader_type': None,
        'trader_type2': None,
        'county': None,
        'loc': None
    }
    list_url = url_path.split('/')
    if list_url[0] == 'mester':
        if len(list_url) == 2:
            county = County.objects.filter(url_key=list_url[1]).first()
            if county is None:
                return empty_list
            else:
                return {
                        'trader_type': None,
                        'trader_type2': None,
                        'county': county.id,
                        'loc': None
                    }

        elif len(list_url) == 3:
            county = County.objects.filter(url_key=list_url[1]).first()
            if county is None:
                return empty_list
            else:
                loc = Loc.objects.filter(url_key=list_url[2]).first()
                if loc is None:
                    return empty_list
                return {
                        'trader_type': None,
                        'trader_type2': None,
                        'county': county.id,
                        'loc': loc.id
                    }
    elif len(list_url) > 4:
        return empty_list
    elif len(list_url) == 1:
        trader_type = TraderType.objects.filter(url_key=list_url[0]).first()
        if trader_type is None:
            return empty_list
        else:
            return {
                'trader_type': trader_type.id,
                'trader_type2': None,
                'county': None,
                'loc': None
            }
    elif len(list_url) == 2:
        trader_type = TraderType.objects.filter(url_key=list_url[0]).first()
        if trader_type is None:
            return empty_list
        else:
            trader_type2 = TraderType.objects.filter(url_key=list_url[1]).first()
            if trader_type2 is None:
                county = County.objects.filter(url_key=list_url[1]).first()
                if county is None:
                    return empty_list
                else:
                    return {
                        'trader_type': trader_type.id,
                        'trader_type2': None,
                        'county': county.id,
                        'loc': None
                    }
            else:
                return {
                        'trader_type': trader_type.id,
                        'trader_type2': trader_type2.id,
                        'county': None,
                        'loc': None
                    }
    elif len(list_url) == 3:
        trader_type = TraderType.objects.filter(url_key=list_url[0]).first()
        if trader_type is None:
            return empty_list
        else:
            county = County.objects.filter(url_key=list_url[1]).first()
            if county is None:
                trader_type2 = TraderType.objects.filter(url_key=list_url[1]).first()
                if trader_type2 is None:
                    return empty_list
                else:
                    county2 = County.objects.filter(url_key=list_url[2]).first()
                    if county2 is None:
                        return empty_list
                    else:
                        return {
                            'trader_type': trader_type.id,
                            'trader_type2': trader_type2.id,
                            'county': county2.id,
                            'loc': None
                        }
            else:
                loc = Loc.objects.filter(url_key=list_url[2]).first()
                if loc is None:
                    return empty_list
                else:
                    return {
                        'trader_type': trader_type.id,
                        'trader_type2': None,
                        'county': county.id,
                        'loc': loc.id
                    }

    elif len(list_url) == 4:
        trader_type = TraderType.objects.filter(url_key=list_url[0]).first()
        if trader_type is None:
            return empty_list

        trader_type2 = TraderType.objects.filter(url_key=list_url[1]).first()
        if trader_type2 is None:
            return empty_list

        county = County.objects.filter(url_key=list_url[2]).first()
        if county is None:
            return empty_list

        loc = Loc.objects.filter(url_key=list_url[3]).first()
        if loc is None:
            return empty_list

        return {'trader_type': trader_type.id,
                'trader_type2': trader_type2.id,
                'county': county.id,
                'loc': loc.id
                }


def search(request, trader_type=None, trader_type2=None, county=None, loc=None):
    url_path = request.path.replace('/cauta/', '')
    trademan_options = get_cache_url(url_path)
    print(trademan_options)
    tradesman_list = Tradesman.approved_objects.all().order_by('-created_at')
    paginator = Paginator(tradesman_list, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    tradsmen = paginator.get_page(page)
    # return_str = "{}- {} - {} - {}".format(trader_type,trader_type2,county,loc)
    return render(request, 'list_tradsmen.html', {'tradsmen': tradsmen,
                                                  'trademan_options':trademan_options
                                                  })


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

