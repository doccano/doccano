import operator
import re

from django.db import models
from django.utils.six.moves import reduce
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.db.models.constants import LOOKUP_SEP


class ExcludeSearchFilter(BaseFilterBackend):
    # The URL query parameter used for the search.
    search_param = api_settings.SEARCH_PARAM
    template = 'rest_framework/filters/search.html'
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
    }
    search_title = _('Search')
    search_description = _('A search term.')

    complex_search_regex = r'^\"(.*)\"\s*(\-)?(.*$)'

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        ret = {
            'terms': None,
            'exclude': None
        }
        params = request.query_params.get(self.search_param, '')
        complex_search_result = re.search(self.complex_search_regex, params)
        print(complex_search_result)
        if (complex_search_result):
            if (complex_search_result.group(1) and complex_search_result.group(2) and complex_search_result.group(3)):
                ret['terms'] = [complex_search_result.group(1)]
                ret['exclude'] = complex_search_result.group(2)
            elif (complex_search_result.group(1) and not complex_search_result.group(2) and complex_search_result.group(3)):
                ret['terms'] = [complex_search_result.group(1), complex_search_result.group(3)]
            else:
                ret['terms'] = [complex_search_result.group(1)]
        else:
            ret['terms'] = params.replace(',', ' ').split()
        return ret

    def construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = 'icontains'
        return LOOKUP_SEP.join([field_name, lookup])

    def must_call_distinct(self, queryset, search_fields):
        """
        Return True if 'distinct()' should be used to query the given lookups.
        """
        for search_field in search_fields:
            opts = queryset.model._meta
            if search_field[0] in self.lookup_prefixes:
                search_field = search_field[1:]
            parts = search_field.split(LOOKUP_SEP)
            for part in parts:
                field = opts.get_field(part)
                if hasattr(field, 'get_path_info'):
                    # This field is a relation, update opts to follow the relation
                    path_info = field.get_path_info()
                    opts = path_info[-1].to_opts
                    if any(path.m2m for path in path_info):
                        # This field is a m2m relation so we know we need to call distinct
                        return True
        return False

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        search_terms_result = self.get_search_terms(request)
        search_terms = search_terms_result['terms']
        search_exclude = None
        if search_terms_result.get('exclude'):
            search_exclude = search_terms_result['exclude']

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(six.text_type(search_field))
            for search_field in search_fields
        ]

        base = queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        
        queryset = queryset.filter(reduce(operator.and_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)
        if search_exclude:
            exclude_conditions = []
            for search_term in search_terms:
                queries = [
                    models.Q(**{orm_lookup: search_term + ' ' + search_exclude})
                    for orm_lookup in orm_lookups
                ]
                exclude_conditions.append(reduce(operator.or_, queries))
            queryset = queryset.exclude(reduce(operator.and_, exclude_conditions))
        return queryset

    def to_html(self, request, queryset, view):
        if not getattr(view, 'search_fields', None):
            return ''

        term = self.get_search_terms(request)
        term = term[0] if term else ''
        context = {
            'param': self.search_param,
            'term': term
        }
        template = loader.get_template(self.template)
        return template.render(context)

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.search_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text(self.search_title),
                    description=force_text(self.search_description)
                )
            )
        ]