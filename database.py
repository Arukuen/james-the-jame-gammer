import json

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


def add_jam(title: str):
    with open('data.json','r+') as f:
        data_dict = json.load(f)
        data_dict['data'].append(title)
        f.seek(0)
        json.dump(data_dict, f, indent = 4)


def fetch()->dict:
    with open('data.json','r') as f:
        data_dict = json.load(f)
        return data_dict

def display():
    print(json.dumps(fetch(), indent = 4, sort_keys=True))


