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
