import pandas as pd
import numpy as np
import networkx as nx


def create_graph_from_edge_list(path, scale=1500):
    # path - path to file with data
    data = pd.read_csv(path)
    st = set()
    weights = {}
    st = list(st)
    tags = list()
    for tag in data['matches']:
        lst = tag.split('#')
        for elem in lst:
            tags.append(elem)
    tmp = np.asarray(tags)
    result = np.unique(tmp, return_counts=True)
    n = len(result[0])
    pop_tags = []
    for i in range(n):
        pop_tags.append((result[0][i], result[1][i]))

    tags = []
    pop_tags = sorted(pop_tags, key=lambda x: -x[1])[120:]
    for elem in pop_tags:
        tags.append(elem[0])
    tags = set(tags)

    n = len(data['id_1'])
    g = nx.Graph()
    g.add_nodes_from(st)
    for i in range(n):
        first = data['id_1'].iloc[i]
        second = data['id_2'].iloc[i]
        tag = data['matches'].iloc[i]
        weight = data['n'].iloc[i]
        for tmp in tag.split('#'):
            if tmp in tags:
                g.add_edge(first, second, weight=weight, matches=tag)
    g.remove_nodes_from(list(nx.isolates(g)))
    pos = nx.spring_layout(g, k = 0.05, iterations=20)
    ids = list(g.nodes())
    x = []
    for elem in ids:
        x.append(pos[elem][0])
    y = []
    for elem in ids:
        y.append(pos[elem][1])

    p = np.empty(shape=(len(x), 2))
    p[:, 0] = np.asarray(x)
    p[:, 1] = np.asarray(y)


    pos_new = nx.rescale_layout(p, scale=scale)

    min_x, max_x = min(pos_new[:, 0]), max(pos_new[:, 0])
    min_y, max_y = min(pos_new[:, 1]), max(pos_new[:, 1])


    pos_new[:, 0] += abs(min_x)
    pos_new[:, 0] /= ((abs(min_x) + max_x) / 1000)

    pos_new[:, 1] += abs(min_y)
    pos_new[:, 1] /= ((abs(min_y) + max_y) / 1000)

    print (pos_new)

    pos = dict()
    for i in range(len(ids)):
        pos[ids[i]] = (pos_new[i][0], pos_new[i][1])
    return g, pos