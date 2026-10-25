import json

def load_data(filepath):

    with open(filepath) as file:

        data = json.load(file)
    return data

        

def get_city(venue):

    address = venue["address"]

    if address == None:
        return None
    
    split_address = address.split(",")

    city = str(split_address[1].strip())

    return city

def get_postcode(venue):

    address = venue["address"]
    
    if address == None:
        return None
    
    split_address = address.split(",")

    postcode = str(split_address[2].strip())

    return postcode