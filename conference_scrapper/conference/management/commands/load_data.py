import json
import os

from django.core.management.base import BaseCommand

from conference_scrapper.conference.models import Conference, ConferenceGraphEdge


def splitter(f):
    for line in f:
        yield line.split("\t")


class Command(BaseCommand):
    help = 'Parses files with raw data and create csv file with edges.'

    def add_arguments(self, parser):
        parser.add_argument('data_dir', nargs='?', type=str, default='data')

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        confs, edges = [], []
        for source in os.listdir(data_dir):
            if source == 'wikicfp.zip': continue
            Conference.objects.filter(source=source).delete()
            ConferenceGraphEdge.objects.filter(source=source).delete()
            with open(f"{data_dir}/{source}/conference_list.json", 'r') as f:
                conf_info = json.load(f)
            for year in os.listdir(f'{data_dir}/{source}'):
                cur_dir = os.path.join(f'{data_dir}/{source}', year)
                if os.path.isdir(cur_dir):
                    with open(os.path.join(cur_dir, "coordinates.csv"), encoding="utf-8") as f:
                        for entry in splitter(f):
                            row = conf_info[entry[0]]
                            confs.append(
                                Conference(
                                    title=row['title'],
                                    url=row['url'],
                                    source=source,
                                    slug=entry[0],
                                    key_words=row['categories'],
                                    description=row['description'],
                                    key_dates=row.get('additional_dates', {}),
                                    x_coord=entry[1],
                                    y_coord=entry[2],
                                    degree=entry[3],
                                    start_date=row['start_date'],
                                    end_date=row['end_date']
                                )
                            )
                    with open(os.path.join(cur_dir, "edge_list.csv"), encoding="utf-8") as f:
                        for entry in splitter(f):
                            edges.append(
                                ConferenceGraphEdge(
                                    conf_1=entry[0],
                                    conf_2=entry[1],
                                    matches_len=entry[2],
                                    matches=entry[3].strip(),
                                    source=source
                                )
                            )
        ConferenceGraphEdge.objects.bulk_create(edges, batch_size=1000)
        Conference.objects.bulk_create(confs, batch_size=1000)
