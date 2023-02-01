import json
from datetime import datetime
from os import path

# Initialize data.json with default setup
# 'data' contains the list of jams
# 'config' contains the configuration
def init():
    data_dict = {
        'data': [],
        'config': {
            'duration': {
                '2 days': [24, 12, 6, 1],
                '1 week': [72, 24, 12, 6, 1],
                '2 weeks': [168, 72, 24, 12, 6, 1]
            },
            'guild_id': -1,
            'channel_id': -1,
            'jammer_role_id': -1,
        }
    }
    with open('data.json', 'w') as f:
        json.dump(data_dict, f, indent = 4)


# Set the configuration of the bot
def set_config(config: str, value: int):
    with open('data.json','r+') as f:
        data_dict = json.load(f)
        data_dict['config'][config] = value
        f.seek(0)
        json.dump(data_dict, f, indent = 4)


# Add the input jam in data.json
def add_jam(title: str, theme: str, date: datetime, duration: str):
    with open('data.json','r+') as f:
        entry = {
                    'title': title,
                    'theme': theme,
                    'date_end': date.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': duration,
                }
        data_dict = json.load(f)
        data_dict['data'].append(entry)
        f.seek(0)
        json.dump(data_dict, f, indent = 4)


# Retuns the config dictionary
def fetch_config(key):
    with open('data.json','r') as f:
        config = json.load(f)['config'][key]
        return config


# Returns a list of all jams from data.json
# Note that dates are in string as this is only use for printing
def fetch_all()->list:
    with open('data.json','r') as f:
        data_dict = json.load(f)['data']
        return data_dict


# Returns the jam with the closest (to the current date) and valid (not yet done) date
# Note that the date is in datetime
def fetch_closest()->dict:
    def update_date(data):
        data['date_end'] = datetime.strptime(data['date_end'], '%Y-%m-%d %H:%M:%S')
        return data

    curr_datetime = datetime.now()

    with open('data.json','r') as f:
        data_dict = json.load(f)['data']
        data_list = map(update_date, data_dict)
        data_list = list(filter(lambda data: data['date_end'] > curr_datetime, data_list))
        if len(data_list) <= 0: return False
        closest_data = min(data_list, key = lambda data: data['date_end'])
        return closest_data


def is_exist()->bool:
    return path.isfile('data.json')


def is_empty()->bool:
    return len(fetch_all()) == 0


# Print the content of data.json in a formatted way
def display():
    print(json.dumps(fetch_all(), indent = 4, sort_keys=True))
