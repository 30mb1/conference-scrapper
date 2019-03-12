import pandas as pd
import json

def create_edge_list(filename, separator='#'):
    
    with open(filename) as f:
        data = json.load(f)    
    edge_list = []
    for i in range(len(data)):
        for j in range(i+1,len(data)):
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
                edge_list.append(edge)
    df = pd.DataFrame(edge_list,columns=['id_1','id_2','n','matches'])
    df.to_csv(filename[:-5]+'.csv',index=False)
    return df

create_edge_list('acm.json')