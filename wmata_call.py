import requests
import json
import pandas as pd
import datetime

# Notes: Consider making bus trip a seperate table

def main():
    api_key = '117e37e796cf4defba0e90b842541bd8'

    url = 'https://api.wmata.com/Bus.svc/json/jBusPositions?api_key={}'.format(api_key)
    df_bus = get_bus(url)

    url = 'https://api.wmata.com/TrainPositions/TrainPositions?contentType=json&api_key={}'.format(api_key)
    df_train = get_train(url)

    # Push to db here
    # df_bus.to_sql('bus_table', db_con, if_exists='append', index=False)
    # df_train.to_sql('train_table', db_con, if_exists='append', index=False)

def get_bus(url):
    # Retrieve
    response = requests.get(url).text
    response_json = json.loads(response)
    df = pd.DataFrame(response_json['BusPositions'])

    # Recode
    col_map = {'BlockNumber': 'blk', 'DateTime': 'dt', 'Deviation': 'deviation',
        'DirectionNum': 'd_num', 'DirectionText': 'd_txt', 'Lat': 'lat',
        'Lon': 'lng', 'RouteID': 'r_id', 'TripEndTime': 't_e',
        'TripHeadsign': 'headsign', 'TripID': 't_id', 'TripStartTime': 't_s',
        'VehicleID': 'v_id'}
    df.rename(col_map, axis=1, inplace=True)
    d_txt_map = {'NORTH': 1, 'SOUTH': 2, 'WEST': 3, 'EAST': 4, 'CLOCKWIS': 5, 'ANTICLKW': 6}
    df['d_txt'] = df['d_txt'].map(d_txt_map)
    for col in ['dt', 't_s', 't_e']:
        df[col] = pd.to_datetime(df[col])
    return df

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
    line_map = {'BL': 1, 'GR': 2, 'OR': 3, 'RD': 4, 'SV': 5, 'YL': 6}
    df['line'].fillna(0, inplace=True)
    df['line'] = df['line'].map(line_map)

    return df

if __name__ == '__main__':
    main()
