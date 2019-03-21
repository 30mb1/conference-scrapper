from django.conf import settings
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from conference_scrapper.conference.filters import ConferenceFilter
from conference_scrapper.conference.models import Conference
from conference_scrapper.conference.utils import get_graph_data


class GraphView(TemplateView):
    template_name = 'graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file = self.kwargs['filename']
        if file not in settings.SOURCE_FILES:
            raise Http404('Url does not exist')

        slug_list = ConferenceFilter(self.request.GET, Conference.objects.all()).qs.values_list('slug', flat=True)

        conf_list, edge_list = get_graph_data(file, ids=slug_list)
        context['conf_list'] = conf_list
        context['edge_list'] = edge_list

        return context


class SearchView(ListView):
    template_name = 'search.html'
    queryset = Conference.objects.all()
    context_object_name = 'conf_objects'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = ConferenceFilter(self.request.GET, queryset).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source = self.request.GET.get('source', 'wikicfp')
        context['data_source'] = source
        context['graph_link'] = f"{source}?{self.request.META['QUERY_STRING']}"
        return context
