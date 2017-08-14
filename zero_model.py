import pandas as pd
import numpy as np

# load google places data
google_data = pd.read_excel("data/google.xlsx", index_col = 0)
google_data['loc_lat'] = list(map(float, google_data['loc_lat'].str.replace(",", ".")))
google_data['loc_lng'] = list(map(float, google_data['loc_lng'].str.replace(",", ".")))
google_data['rating'] = list(map(float, google_data['rating'].str.replace(",", ".")))
google_data['rid'] = google_data.index.get_values()

# get McDonalds and similar by types list places
mc_data = google_data[(google_data['name'].str.contains("McDon|Mcdon", na = False)) | (google_data['types'] == "restaurant, food, point_of_interest, establishment")]

# get near places by type
def places_near(row):
    place_types = ["accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar",
                   "beauty_salon", "bicycle_store",
                   "book_store", "bowling_alley", "bus_station", "cafe", "campground", "car_dealer", "car_rental",
                   "car_repair", "car_wash", "casino", "cemetery",
                   "church", "city_hall", "clothing_store", "convenience_store", "courthouse", "dentist",
                   "department_store", "doctor", "electrician", "electronics_store",
                   "embassy", "fire_station", "florist", "funeral_home", "furniture_store", "gas_station", "gym",
                   "hair_care", "hardware_store", "hindu_temple",
                   "home_goods_store", "hospital", "insurance_agency", "jewelry_store", "laundry", "lawyer", "library",
                   "liquor_store", "local_government_office",
                   "locksmith", "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater",
                   "moving_company", "museum", "night_club",
                   "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber", "police",
                   "post_office", "real_estate_agency", "restaurant",
                   "roofing_contractor", "rv_park", "school", "shoe_store", "shopping_mall", "spa", "stadium",
                   "storage", "store", "subway_station", "synagogue",
                   "taxi_stand", "train_station", "transit_station", "travel_agency", "university", "veterinary_care",
                   "zoo"]
    radius_list = [1000]

    rid = row['rid'].item()
    ndat = google_data[google_data['rid'] != rid]
    pdat = pd.DataFrame(columns=('rid', 'radius', 'type', 'count', 'avg_rank'))
    for r in radius_list:
        for type in place_types:
            tdat = ndat[(ndat['types'].str.contains(type, na=False))]
            lat_min = tdat['loc_lat']
            lng_min = tdat['loc_lng']
            lat_max = mc_data[mc_data['rid'] == rid]['loc_lat']
            lng_max = mc_data[mc_data['rid'] == rid]['loc_lng']
            tdat = tdat.assign(radius=0.5 * 111000 * ((lat_min - lat_max) ** 2 + 0.5 * ((lng_min - lng_max) ** 2) * (
                (np.cos(lat_min * 2 * np.arcsin(1) / 180)) ** 2 + (
                np.cos(lat_max * 2 * np.arcsin(1) / 180)) ** 2)) ** 0.5)
            tdat = tdat[tdat['radius'] <= r]
            pdat = pdat.append(pd.DataFrame({'rid': [rid], 'radius': [r], 'type': [type], 'count': [tdat.shape[0]],
                                             'avg_rank': [np.mean(tdat['rating'])]}))
    return pdat


pdat = mc_data.groupby(by='rid', group_keys=False).apply(places_near)



