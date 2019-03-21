import json
from collections import Counter

import networkx as nx
import pandas as pd
from django.core.management.base import BaseCommand
from conference_scrapper.conference.models import Conference, ConferenceEdge

class Command(BaseCommand):
    help = 'Parses files with raw data and create csv file with edges.'

    def add_arguments(self, parser):
        parser.add_argument('filenames', nargs='+', type=str)

    def handle(self, *args, **options):
        filenames, separator = options['filenames'], '#'
        for name in filenames:
            # flush all previous data for this source
            Conference.objects.filter(source=name[:-5]).delete()
            ConferenceEdge.objects.filter(source=name[:-5]).delete()
            conf_to_create, edge_to_create = [], []
            with open(f'data/{name}') as f:
                data = json.load(f)
            edge_list = []
            for i in range(len(data)):
                row = data[i]
                conf_to_create.append(
                    Conference(
                        title=row['title'],
                        url=row['url'],
                        source=name[:-5],
                        slug=row['id'],
                        key_words=row['categories'],
                        description=row['description']
                    )
                )
                for j in range(i + 1, len(data)):
                    matches = list(set(data[i]['categories']).intersection(data[j]['categories']))
                    if (separator in str(matches)):
                        print("Separator '" + separator + "' is used in categories: " + str(matches))
                        return -1
                    if (len(matches) != 0):
                        edge = {'id_1': data[i]['id'],
                                'id_2': data[j]['id'],
                                'n': str(len(matches)),
                                'matches': separator.join(map(lambda x: x.strip(), matches))
                                }
                        edge_to_create.append(
                            ConferenceEdge(
                                conf_1=edge['id_1'],
                                conf_2=edge['id_2'],
                                matches_len=edge['n'],
                                matches=edge['matches'],
                                source=name[:-5]
                            )
                        )
                        edge_list.append(edge)
            df = pd.DataFrame(edge_list, columns=['id_1', 'id_2', 'n', 'matches'])
            Conference.objects.bulk_create(conf_to_create, batch_size=100)
            ConferenceEdge.objects.bulk_create(edge_to_create, batch_size=1000)

            tags = []
            for tag in df['matches']:
                tags += tag.split('#')

            counts = Counter(tags)
            # get rid of first 120 most popular tags
            active_tags = sorted(set(tags), key=lambda x: counts[x], reverse=True)[120:]

            g = nx.Graph()
            for i, (first, second, weight, tag) in df.iterrows():
                [g.add_edge(first, second, weight=weight, matches=tag) for j in tag.split('#') if j in active_tags]

            g.remove_nodes_from(list(nx.isolates(g)))
            pos = nx.spring_layout(g, k=0.05, iterations=20)
            ids = list(g.nodes())

            degrees = {node: value for node, value in g.degree()}
            degree = [degrees[elem] for elem in ids]
            x = [pos[elem][0] for elem in ids]
            y = [pos[elem][1] for elem in ids]

            d = {'id': ids, 'x': x, 'y': y, 'degree': degree}
            df = pd.DataFrame(data=d)
            df.to_csv(f'data/{name[:-5]}_coordinates.csv', index=False)
