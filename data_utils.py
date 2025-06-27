import json

DROPDOWN_FILE = 'data/dropdown_data.json'

def get_dropdown_data():
    with open(DROPDOWN_FILE, 'r') as f:
        return json.load(f)

def add_entry(category, field, value):
    with open(DROPDOWN_FILE, 'r') as f:
        data = json.load(f)

    if value not in data[category][field]:
        data[category][field].append(value)

        with open(DROPDOWN_FILE, 'w') as f:
            json.dump(data, f, indent=4)
