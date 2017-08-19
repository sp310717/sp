import requests
import pandas as pd

cookie = {'eway_session': 'f53453598174519c284b45614e7154dd',
          'new_full_version': '1',
          'city[key]': 'kyiv',
          'lang': 'ua',
          'mapProvider5': 'Google',
          '_ga': 'GA1.3.1976271195.1502126539',
          '_gid': 'GA1.3.464638752.1503080548'}
headers = {'X-Requested-With': 'XMLHttpRequest'}
cities = {
    'bilatserkva': 'Біла Церква',
    'boryspil': 'Бориспіль',
    'dnipropetrovsk': 'Дніпро',
    'vinnytsia': 'Вінниця',
    'zaporizhzhya': 'Запоріжжя',
    'frankivsk': 'Івано-Франківськ',
    'lviv': 'Львів',
    'odesa': 'Одеса',
    'rivne': 'Рівне',
    'kharkiv': 'Харків',
    'kherson': 'Херсон',
    'kyiv': 'Київ'
}
routes_info = []
for city in cities.keys():
    print(city)
    resp = requests.get('https://www.eway.in.ua/ajax/ua/{0}/routes'.format(city), cookies=cookie, headers=headers)
    routes_id = []
    for transport_type in resp.json().keys():
        current_type = resp.json().get(transport_type)
        for item in current_type:
            routes_id.append(item.get('ri'))
        print('type: {0}, count: {1}'.format(transport_type, str(len(current_type))))

    for id in routes_id:
        try:
            resp = requests.get('https://www.eway.in.ua/ajax/ua/{0}/routeInfo/'.format(city) + str(id), cookies=cookie,
                                headers=headers).json()
            try:
                title = resp.get('general').get('page_title').split(', схема')[0].replace(';','')
            except:
                title = ''
            try:
                type = resp.get('general').get('tn').replace(';','')
            except:
                type = ''
            try:
                begin_lat = resp.get('begin').get('x')
            except:
                begin_lat = ''
            try:
                begin_lon = resp.get('begin').get('y')
            except:
                begin_lon = ''
            try:
                end_lat = resp.get('end').get('x')
            except:
                end_lat = ''
            try:
                end_lon = resp.get('end').get('y')
            except:
                end_lon = ''
            try:
                forward = resp.get('scheme').get('forward')
            except:
                forward = ''
            try:
                backward = resp.get('scheme').get('backward')
            except:
                backward = ''
            routes_info.append(
                [cities.get(city), title, type, begin_lat, begin_lon, end_lat, end_lon, forward, backward])
        except:
            print('bad route')
    pd.DataFrame(routes_info,
                 columns=['city', 'title', 'type', 'begin_lat', 'begin_lon', 'end_lat', 'end_lon', 'forward',
                          'backward']).to_csv('routes_info.csv', sep=';')
