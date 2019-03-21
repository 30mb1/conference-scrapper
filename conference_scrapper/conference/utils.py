import pandas as pd


def get_graph_data(filename):
    edge_data = pd.read_csv(f'data/{filename}.csv')
    coordinates = pd.read_csv(f'data/{filename}_coordinates.csv')

    conf_list, title_to_id = [], {}
    for i, (short_title, x, y, degree) in coordinates.iterrows():
        conf_list.append([x, y, i, {'title': short_title, 'degree': degree}])
        title_to_id[short_title] = i

    edge_list = []
    for i, (id_1, id_2, weight, matches) in edge_data.iterrows():
        if id_1 in title_to_id and id_2 in title_to_id:
            edge_list.append([title_to_id[id_1], title_to_id[id_2], weight, {}])

    return conf_list, edge_list
