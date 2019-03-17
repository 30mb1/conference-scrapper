from django.views.generic.base import TemplateView
from conference_scrapper.conference.utils import create_graph_from_edge_list

class GraphView(TemplateView):
    template_name = 'Graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file = self.kwargs['filename']
        g, pos = create_graph_from_edge_list(f'data/{file}.csv')


        edge_list = {}
        for num, (from_, to_) in enumerate(list(g.edges)):
            edge = g[from_][to_]
            edge_list[num+1] = (from_, to_, edge['weight'], edge['matches'])

        conf_list = {}
        for key, value in pos.items():
            conf_list[key] = (key, value[0], value[1])

        context['conf_list'] = conf_list
        context['edge_list'] = edge_list
        context['vert_radius'] = 20
        context['edge_width'] = 5
        return context
