from conference_scrapper.conference.models import ConferenceGraphEdge, Conference
import networkx as nx
from statistics import mean


def get_graph_data(slugs=None):
    conf_list_db = (Conference
                    .objects
                    .filter(slug__in=slugs)
                    .values('x_coord', 'y_coord', 'id', 'degree', 'slug'))
    conf_list, title_to_id = [], {}

    for i in conf_list_db:
        conf_list.append(
            [i['x_coord'], i['y_coord'], i['id'], {'title': i['slug'], 'degree': i['degree']}]
        )
        title_to_id[i['slug']] = i['id']

    edges = ConferenceGraphEdge.objects.filter(conf_1__in=slugs, conf_2__in=slugs)
    edge_list = [
        [title_to_id[i.conf_1], title_to_id[i.conf_2], i.matches_len, i.matches] for i in edges
    ]

    return conf_list, edge_list


def get_graph_meta(conf_list, edge_list):
    g = nx.Graph()
    for i in conf_list:
        g.add_node(i[2])

    for i in edge_list:
        g.add_edge(i[0], i[1])

    graph_info = {}

    graph_info['degree'] = mean([i[1] for i in nx.degree(g)])
    graph_info['density'] = nx.classes.function.density(g)
    graph_info['degree_centrality'] = mean(nx.algorithms.centrality.degree_centrality(g).values())
    graph_info['closeness_centrality'] = mean(nx.algorithms.centrality.closeness_centrality(g).values())
    graph_info['betweenness_centrality'] = mean(nx.algorithms.centrality.betweenness_centrality(g).values())

    return graph_info
