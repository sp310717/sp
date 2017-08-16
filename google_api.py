import numpy as np
import pandas as pd
import requests
import time
#https://maps.googleapis.com/maps/api/place/radarsearch/json?
# location=50.283008, 28.648010&radius=5000&type=car_repair&key=AIzaSyDomUhpqCrAOofZwNYxZRecDD0yo2uudu4
#
# df = pd.read_csv('city_location')

def get_places_list(lat, lon, radius, type):
    query = 'https://maps.googleapis.com/maps/api/place/radarsearch/' \
            'json?location={0},{1}&radius={2}&type={3}&key=AIzaSyDomU' \
            'hpqCrAOofZwNYxZRecDD0yo2uudu4'\
        .format(lat, lon, str(radius), type)
    is_ok = False
    requests_cnt = 0
    places_list = []
    while (not is_ok) & (requests_cnt < 3):
        respons = requests.get(query)
        if respons.status_code == 200:
            is_ok = True
            places = respons.json().get('results')
            for place in places:
                place_id = place.get('place_id')
                places_list.append(place_id)
        else:
            requests_cnt += 1
            time.sleep(60)
    return places_list

def get_place_details(plaice_id, city_key, city_name, type):
    query = 'https://maps.googleapis.com/maps/api/place/details/json?' \
            'placeid={0}&key=AIzaSyDomUhpqCrAOofZwNYxZRecDD0yo2uudu4'\
        .format(plaice_id)


    is_ok = False
    requests_cnt = 0
    while (not is_ok) & (requests_cnt < 3):
        res = requests.get(query)

        name = ''
        address = ''
        website = ''
        rating = ''
        phone = ''
        p_lat = ''
        p_lon = ''
        if res.status_code == 200:
            respons = res.json().get('result')
            is_ok = True
            name = respons.get('name')
            address = respons.get('formatted_address')
            website = respons.get('website')
            rating = respons.get('rating')
            phone = respons.get('international_phone_number')
            p_lat = respons.get('geometry').get('location').get('lat')
            p_lon = respons.get('geometry').get('location').get('lng')
        else:
            requests_cnt += 1
            time.sleep(60)
    return [city_key, city_name, type, plaice_id, name, address, website, rating, phone, p_lat, p_lon]

types = ['car_dealer', 'car_rental', 'car_repair', 'car_wash', 'parking', 'gas_station']

df = pd.read_csv('cities.csv', sep=';')
all_places = []
for i in range(38, len(df)):
    city_key = df.iloc[i].values[0]
    city_name = df.iloc[i].values[1]
    lat = df.iloc[i].values[3].replace(',', '.')
    lon = df.iloc[i].values[2].replace(',', '.')
    for type in types:
        places = get_places_list(lat, lon, 50000, type)
        print('city: {0}, type: {1}, places_leng: {2}'.format(city_name, type, str(len(places))))
        for place in places:
            all_places.append(get_place_details(place, city_key, city_name, type))
    df1 = pd.DataFrame(all_places)
    df1.columns = ['city_key', 'city_name', 'type', 'plaice_id', 'name', 'address', 'website', 'rating', 'phone', 'lat', 'lon']
    df1 = df1.fillna('NaN')
    df1.to_csv('all_places_2.csv', index = False)





