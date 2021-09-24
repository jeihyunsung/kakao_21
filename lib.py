def parse_location_token(token):
    parsed_location = {}
    locations = token['locations']
    for x in locations:
        parsed_location[x['id']] = x['located_bikes_count']
    return parsed_location

def parse_trucks_token(token):
    parsed_trucks_location = {}
    parsed_trucks_bikes = {}
    trucks = token['trucks']
    for x in trucks:
        parsed_trucks_location[x['id']] = x['location_id']
        parsed_trucks_bikes[x['id']] = x['loaded_bikes_count']
    return parsed_trucks_location, parsed_trucks_bikes