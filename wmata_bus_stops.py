import requests
import json
import pandas as pd
import numpy as np
import private


def main():
    # Ping WMATA
    api_keys = private.wmata_keys()
    api_key = api_keys['primary']
    url = 'https://api.wmata.com/Bus.svc/json/jStops?api_key={}'.format(api_key)
    df_list = get_stops(url)
    df_s = df_list[0]
    df_sr = df_list[1]

    # Push to db here
    engine = private.connect_db()
    df_s.to_sql('wmata_bus_stop', engine, if_exists='replace', index=False)
    df_sr.to_sql('wmata_bus_sr', engine, if_exists='replace', index=False)

def get_stops(url):
    # Retrieve
    response = requests.get(url).text
    response_json = json.loads(response)
    df = pd.DataFrame(response_json['Stops'])
    # Recode
    col_map = {'StopID': 's_id', 'Name': 's_name', 'Lat': 'lat', 'Lon': 'lng', 'Routes': 'r_id'}
    df.rename(col_map, axis=1, inplace=True)
    df['s_id'] = df['s_id'].astype(float)
    # Handle duplicate stop ids
    stop_id_map = {'BUS COLLECTION POINT I/B': 0, 'ANNOUNCEMENT STOP + WEST END OF HOV - RTE 236': 1,
        'MARK CENTER OUTBOUND STOP': 2, 'NAYLOR RD STA OUTBOUND': 3, 'SSTC LL COLLECTION POINT I/B': 4,
        'SSTC LL COLLECTION POINT I/B': 5, 'SSTC ML COLLECTION POINT I/B': 6, 'Z11 EXPRESS ANOUNCEMENT': 7}
    df.loc[df['s_id']==0, 's_id'] = df.loc[df['s_id']==0, 's_name'].map(stop_id_map)

    # Split into two tables
    df_s = df[['s_id', 's_name', 'lat', 'lng']]
    df_sr = df[['s_id', 'r_id']]
    df_sr = pd.DataFrame({
        col:np.repeat(df_sr[col].values, df_sr['r_id'].str.len())
        for col in df_sr.columns.difference(['r_id'])
    }).assign(**{'r_id':np.concatenate(df_sr['r_id'].values)})[df_sr.columns.tolist()]
    df_list = [df_s, df_sr]
    return df_list

if __name__ == '__main__':
    main()
