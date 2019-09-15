import requests
import json
import pandas as pd
import datetime
import private as private
import pdb
# import sqlite3
# from sqlite3 import Error

# Notes: Consider making bus trip a seperate table

def main():
    # Ping WMATA
    api_keys = private.wmata_keys()
    api_key = api_keys['primary']
    url = 'https://api.wmata.com/TrainPositions/TrainPositions?contentType=json&api_key={}'.format(api_key)
    df = get_train(url)
    # print(df.head())

    # Push to db here
    engine = private.connect_db()
    df.to_sql('wmata_train', engine, if_exists='append', index=False)

def get_train(url):
    # Retrieve
    response = requests.get(url).text
    response_json = json.loads(response)
    df = pd.DataFrame(response_json['TrainPositions'])

    # Recode
    df['dt'] = datetime.datetime.now()
    col_map = {'CarCount': 'cars', 'CircuitId': 'c_id',
        'DestinationStationCode': 'dest_station', 'DirectionNum': 'd_num',
        'LineCode': 'line', 'SecondsAtLocation': 'sec_loc',
        'ServiceType': 'service', 'TrainId': 't_id', 'TrainNumber': 't_num'}
    df.rename(col_map, axis=1, inplace=True)

    pdb.set_trace()

    return df

if __name__ == '__main__':
    main()
