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

    url = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/All?api_key=' + api_key
    df = get_train_predictions(url)

    print(df.head())

    # Push to db here
    #engine = private.connect_db()
    #df.to_sql('wmata_train_pred', engine, if_exists='append', index=False)

def get_train_predictions(url):
    # Retrieve
    response = requests.get(url).text
    response_json = json.loads(response)
    df = pd.DataFrame(response_json['Trains'])

    # Recode
    col_map = {'DestinationCode':'dest_station','Line':'line',
    'LocationCode':'loc_code','Min':'min','Car':'cars','Group':'group'}

    df.rename(col_map, axis=1, inplace=True)

    df['retrieved'] = datetime.datetime.now()

    # Filter to specific variables

    df = df[['dest_station','line','loc_code','min','cars']]

    return df

if __name__ == '__main__':
    main()