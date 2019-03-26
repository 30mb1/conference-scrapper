from statistics import mean

import networkx as nx
from numpy import empty, asarray
from numpy.random import seed, exponential

from conference_scrapper.conference.models import ConferenceGraphEdge, Conference


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

seed(154)
canvas_size = 1000
padding = 20

g = nx.gnm_random_graph(50, 100)
ws = exponential(size=g.number_of_edges())
edge_list_n = {}
for i, (u, v, w) in enumerate(g.edges(data=True)):
    tw = (round(ws[i]) % 4) + 1
    w['weight'] = tw
    edge_list_n[i] = (u, v, tw, "")

pos = nx.kamada_kawai_layout(g)

degrees = dict()
for node, val in g.degree():
    degrees[node] = val
ids = list(g.nodes())


x = []
y = []
degree = []
for elem in ids:
    degree.append(degrees[elem])
    x.append(pos[elem][0])
    y.append(pos[elem][1])

p = empty(shape=(len(x), 2))
p[:, 0] = asarray(x)
p[:, 1] = asarray(y)
scale = canvas_size // 2 - padding
pos_new = nx.rescale_layout(p, scale=scale)
pos = dict()
for i in range(len(ids)):
    pos[ids[i]] = (pos_new[i][0], pos_new[i][1])
    x[i] = pos_new[i][0] + scale + padding
    y[i] = pos_new[i][1] + scale + padding
conf_list_n = {Id: (X, Y, Degree) for Id, X, Y, Degree in zip(ids, x, y, degree)}

max_weight = 4
time_desease = dict()
for i in ids:
    time_desease[i] = 2