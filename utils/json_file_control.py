import json


def load_json_file(path):
    json_file = open(path)
    json_data = json.load(json_file)
    json_file.close()
    return json_data
