import json
from datetime import datetime

def init():
    data_dict = {
        'data': [],
        'config': {
            'duration': {
                '2 days': [24, 12, 6, 1],
                '1 week': [72, 24, 12, 6, 1],
                '2 weeks': [168, 72, 24, 12, 6, 1]
            }
        }
    }
    with open('data.json', 'w') as f:
        json.dump(data_dict, f, indent = 4)


def add_jam(title: str, theme: str, date: datetime, duration: str):
    with open('data.json','r+') as f:
        entry = {'title': title, 'theme': theme, 'date': date, 'duration': duration}
        data_dict = json.load(f)
        data_dict['data'].append(entry)
        f.seek(0)
        json.dump(data_dict, f, indent = 4, default = str)


def fetch(is_config = False)->dict:
    with open('data.json','r') as f:
        if is_config:
            data_dict = json.load(f)['config']
        else:
            data_dict = json.load(f)['data']
        return data_dict


def fetch_all()->dict:
    pass

def fetch_close()->dict:
    pass

def display():
    print(json.dumps(fetch(), indent = 4, sort_keys=True))


init()
add_jam('title', 'theme', datetime.now(), 'amogus')
display()