import queue

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from numpy.random import binomial

from conference_scrapper.conference.filters import ConferenceFilter
from conference_scrapper.conference.utils import *


class GraphView(TemplateView):
    template_name = 'graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_list = ConferenceFilter(self.request.GET, Conference.objects.all()).qs.values_list('slug', flat=True)

        conf_list, edge_list = get_graph_data(slugs=slug_list)
        context['conf_list'] = conf_list
        context['edge_list'] = edge_list
        context['graph_info'] = get_graph_meta(conf_list, edge_list)
        return context


class NickGrpah(TemplateView):
    template_name = 'graph2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['conf_list'] = conf_list_n
        context['edge_list'] = edge_list_n
        context['canvas_width'] = 1000
        context['canvas_height'] = 1000
        context['vert_radius'] = 4
        context['edge_width'] = 1
        return context

@method_decorator(csrf_exempt, name='dispatch')
class GameView(View):
    def post(self, request, *args, **kwargs):
        vertex = kwargs['vertex']
        if not vertex:
            return ""
        vertex = int(vertex)

        rez = dict()
        q = queue.Queue()
        q.put(vertex)
        count = 0
        max_count = 0
        rez[vertex] = count
        time_desease[vertex] = 2
        rez_removed = dict()
        while q.empty() == False:
            node = q.get()
            count = rez[node]
            if count > max_count:
                max_count = count

            for elem in time_desease.keys():
                if elem in rez.keys() and elem != node:
                    time_desease[elem] -= 1
                    if time_desease[elem] == 0:
                        rez_removed[elem] = rez[elem] + 2

            for elem in g.neighbors(node):
                if elem not in rez.keys():
                    if g.has_edge(node, elem):
                        probability = g.get_edge_data(node, elem)['weight'] / max_weight
                        p = binomial(1, probability, 1)
                        if p == 1 and node in rez.keys() and node not in rez_removed.keys():
                            q.put(elem)
                            rez[elem] = count + 1
                            time_desease[elem] = 2
        for val in rez_removed.values():
            max_count = max(max_count, val)

        answer = [[] for i in range(max_count * 2 + 2)]

        for key in rez.keys():
            answer[rez[key] * 2].append(key)
        for key in rez_removed.keys():
            if (rez_removed[key] * 2 + 1) < (max_count * 2 + 2):
                answer[rez_removed[key] * 2 + 1].append(key)
        return HttpResponse('\n'.join(map(lambda x: "\t".join(map(str, x)), answer)))


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


class DownloadView(View):
    def get(self, request, *args, **kwargs):
        zip_file = open('/initial_data/wikicfp.zip', 'rb')
        response = HttpResponse(zip_file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=wikicfp.zip'
        return response