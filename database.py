import json
from datetime import datetime
from pprint import pprint

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
            }
        }
    }
    with open('data.json', 'w') as f:
        json.dump(data_dict, f, indent = 4)

# Write the input jam in data.json
def add_jam(title: str, theme: str, date: datetime, duration: str):
    with open('data.json','r+') as f:
        entry = {'title': title, 'theme': theme, 'date': date.strftime('%Y-%m-%d %H:%M:%S'), 'duration': duration}
        data_dict = json.load(f)
        data_dict['data'].append(entry)
        f.seek(0)
        json.dump(data_dict, f, indent = 4)


# Retuns the config dictionary
def fetch_config(is_config = False)->dict:
    with open('data.json','r') as f:
        config_dict = json.load(f)['config']
        return config_dict


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
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        return data

    curr_datetime = datetime.now()

    with open('data.json','r') as f:
        data_dict = json.load(f)['data']
        data_list = map(update_date, data_dict)
        data_list = list(filter(lambda data: data['date'] > curr_datetime, data_list))
        if len(data_list) <= 0: return False
        closest_data = min(data_list, key = lambda data: data['date'])
        return closest_data


# Print the content of data.json in a formatted way
def display():
    print(json.dumps(fetch_all(), indent = 4, sort_keys=True))

