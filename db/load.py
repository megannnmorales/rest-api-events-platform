import json

def load_data(filepath):

    with open(filepath) as file:

        data = json.load(file)
    return data

        

