from django_filters import CharFilter, FilterSet, DateFilter

from conference_scrapper.conference.models import Conference


class ConferenceFilter(FilterSet):
    query = CharFilter(method='filter_query')
    date = DateFilter(method='filter_date')
    source = CharFilter(method='filter_source')

    class Meta:
        model = Conference
        fields = ['source', 'date', 'query']

    def filter_query(self, queryset, name, value):
        filter_type = self.data.get('filter_type', 'tags')
        if filter_type == 'tags':
            return self.filter_tags(queryset, name, value)
        elif filter_type == 'title':
            return self.filter_title(queryset, name, value)
        elif filter_type == 'url':
            return self.filter_url(queryset, name, value)
        else:
            return queryset

    def filter_date(self, queryset, name, value):
        queryset = queryset.filter(start_date__lte=value, end_date__gte=value)
        return queryset

    def filter_title(self, queryset, name, value):
        queryset = queryset.filter(title__iexact=value)
        return queryset

    def filter_tags(self, queryset, name, value):
        tags = [x.strip() for x in value.split(',')]
        use_all_tags = self.data.get('use_all_tags', 'true') == 'true'

        if use_all_tags:
            queryset = queryset.filter(key_words__contains=tags)
        else:
            queryset = queryset.filter(key_words__overlap=tags)
        return queryset

    def filter_url(self, queryset, name, value):
        queryset = queryset.filter(url=value)
        return queryset

    def filter_source(self, queryset, name, value):
        if value == 'all':
            return queryset
        else:
            return queryset.filter(source=value)

