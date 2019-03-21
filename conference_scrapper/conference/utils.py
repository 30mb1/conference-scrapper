import pandas as pd
from time import time
from conference_scrapper.conference.models import ConferenceEdge


def get_graph_data(filename, ids=None):
    coordinates = pd.read_csv(f'data/{filename}_coordinates.csv')
    slug_dict = {i: True for i in ids}

    conf_list, title_to_id = [], {}
    for i, (short_title, x, y, degree) in coordinates.iterrows():
        if short_title in slug_dict:
            conf_list.append([x, y, i, {'title': short_title, 'degree': degree}])
            title_to_id[short_title] = i

    conf_ids = list(title_to_id.keys())
    all_edges = ConferenceEdge.objects.filter(conf_1__in=conf_ids, conf_2__in=conf_ids)

    edge_list = []
    for edge in all_edges:
        edge_list.append([title_to_id[edge.conf_1], title_to_id[edge.conf_2], edge.matches_len, edge.matches])

    return conf_list, edge_list
