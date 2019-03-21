from django.views.generic.base import TemplateView
from conference_scrapper.conference.utils import get_graph_data
from django.conf import settings
from django.http import Http404
from conference_scrapper.conference.models import Conference
from django.views.generic import ListView
from conference_scrapper.conference.filters import ConferenceFilter

class GraphView(TemplateView):
    template_name = 'graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()

        file = self.kwargs['filename']
        if file not in settings.SOURCE_FILES:
            raise Http404('Url does not exist')

        conf_list, edge_list = get_graph_data(file)
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
        # params = self.request.GET.copy()
        #
        # q = ConferenceFilter(self.request.GET, self.queryset)
        #
        # tags = [x.strip() for x in params.get('tags', '').split(',')]
        # objects = Conference.objects.filter(key_words__contains=tags)
        # # context['objects'] = objects
        # context['graph_link'] = f"acm/?tags={','.join(tags)}"

        return context