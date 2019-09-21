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

def prior_stops():
    c_dict = {
        'Georgia Avenue / 7th Street (DC)': ['70', '74', '70v1', '79'],
        'Wisconsin Avenue / Pennsylvania Avenue': ['31', '32', '32v1', '34', '36', '37', '39'],
        'Sixteenth Street': ['S1', 'S2', 'S2v1', 'S4', 'S9'],
        'H Street / Benning Road': ['X1', 'X2', 'X2v1', 'X2v2', 'X2v3', 'X3', 'X3v1', 'X9', 'X9v1', 'X9v2'],
        'U Street / Garfield': ['90', '90v1', '90v2', '92', '92v1', '92v2', '93'],
        'Anacostia / Congress Heights': ['A2', 'A2v1', 'A2v2', 'A2v3','A4', 'A4v1', 'A4v2', 'A4v3', 'A4v4', 'A4v5', 'A5','A6', 'A6v1', 'A7', 'A8', 'A8v1', 'A9', 'A42','A46','A48'],
        'Fourteenth Street': ['52', '52v1', '52v2', '53','54', '54v1', '54v2', '54v3'],
        'North Capitol Street': ['80', '80v1', '80v2', '80v3'],
        'Rhode Island Avenue': ['G8', 'G8v1', 'G8v2', 'G8v3'],
        'University Boulevard / East-West Highway': ['J1', 'J1v1', 'J2', 'J2v1', 'J2v2', 'J3', 'J4'],
        'Southern Avenue Metro - National Harbor': ['NH1'],
        'Veirs Mill Road': ['Q1', 'Q2', 'Q2v1', 'Q2v2', 'Q4', 'Q4v1', 'Q5', 'Q6', 'Q6v1'],
        'New Hampshire Avenue': ['K6', 'K6v1', 'K9', 'K9v1'],
        'Georgia Avenue (MD)': ['Y5', 'Y7', 'Y8', 'Y9'],
        'East-West Highway': ['F4', 'F4v1', 'F4v2', 'F6', 'F6v1', 'F6v2'],
        'Greenbelt / Twinbrook': ['C2', 'C2v1', 'C2v2', 'C2v3', 'C4', 'C4v1', 'C4v2', 'C4v3'],
        'Rhode Island Avenue Metro to Laurel': ['81', '82', '83', '83v1', '83v2', '83v3', '83v4', '86', '86v1', '86v2', '87', '87v1', '87v2', '87v3', '87v4', '87v5', '88', '89', '89M', '89v1'],
        'Eastover / Addison Road': ['P12', 'P12v1', 'P12v2'],
        'Colesville Road / Columbia Pike (MD US29)': ['Z2', 'Z2v1', 'Z2v2', 'Z2v3', 'Z6', 'Z6v1', 'Z6v2', 'Z8', 'Z8v1', 'Z8v2', 'Z8v3', 'Z8v4', 'Z8v5', 'Z8v6', 'Z9','Z29','Z11', 'Z11v1', 'Z13'],
        'Richmond Hwy Express (REX)': ['REX', 'REXv1', 'REXv2', 'REXv3', 'REXv4'],
        'Columbia Pike (Pike Ride)': ['16A', '16B','16D','16E','16F','16J','16C', '16Cv1', '16G', '16Gv1', '16H', '16L', '16Y', '16Yv1'],
        'Crystal City / Potomac Yard': ['10A', '10B', '10E', '10N'],
        'Leesburg Pike': ['28A', '28Av1', '28F', '28G'],
        'Little River Tpke / Duke St': ['29C', '29G', '29K', '29Kv1', '29N', '29Nv1', '29W']
    }

if __name__ == '__main__':
    main()
