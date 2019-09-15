import requests
import json
import pandas as pd
import datetime
import private
import re
# import sqlite3
# from sqlite3 import Error

# Notes: Consider making bus trip a seperate table

def main():
    # Ping WMATA
    api_keys = private.wmata_keys()
    api_key = api_keys['primary']

    stop_ids = ['1001195'] ## placeholder

    for stop in stop_ids:

        url = 'https://api.wmata.com/NextBusService.svc/json/jPredictions?StopID=' + stop + '&api_key=' + api_key
        df = get_bus_predictions(url,stop)
        # print(df.head())

        # Push to db here
        engine = private.connect_db()
        df.to_sql('wmata_bus_pred', engine, if_exists='append', index=False)

def get_bus_predictions(url,stop_id):
    # Retrieve
    response = requests.get(url).text
    response_json = json.loads(response)
    df = pd.DataFrame(response_json['Predictions'])
    df['s_id'] = stop_id

    # Recode
    col_map = {'DirectionNum': 'd_num', 'DirectionText': 'd_txt', 'RouteID': 'r_id',
        'TripID': 't_id','VehicleID': 'v_id','Minutes':'min'}

    df.rename(col_map, axis=1, inplace=True)

    df['d_txt'] = df['d_txt'].str.extract(pat='(^North|^South|^West|^East)')
    d_txt_map = {'North': 1, 'South': 2, 'West': 3, 'East': 4}
    df['d_txt'] = df['d_txt'].map(d_txt_map)
    df['retrieved'] = datetime.datetime.now()

    return df

if __name__ == '__main__':
    main()
