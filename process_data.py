import numpy as np
import pandas as pd
import os
import glob


def merge_hisrec_daily(userpath,stationnumber):
    histpath = os.path.join(userpath, 'pub','CDC','observations_germany','climate','daily','kl','historical')
    recpath  = os.path.join(userpath, 'pub','CDC','observations_germany','climate','daily','kl','recent')

    histfile_tmp = os.path.join(histpath, "produkt_klima_tag_*")
    histfile_tmp += str(stationnumber).zfill(5)+'.txt'
    histfile = glob.glob(histfile_tmp)[0]

    recfile_tmp = os.path.join(recpath, "produkt_klima_tag_*")
    recfile_tmp += str(stationnumber).zfill(5)+'.txt'
    recfile = glob.glob(recfile_tmp)[0]

    histdata = pd.read_table(histfile, sep=";", low_memory=False)
    recentdata = pd.read_table(recfile, sep=";", low_memory=False)
    merged=pd.concat([histdata,recentdata])
    return merged

def clean_merged_daily(merged):
    merged_clean = merged.replace(-999, np.nan, regex=True)
    merged_clean = merged_clean.drop(['eor'],axis=1)

    merged_clean.columns =['Station_ID','Date','Quality_of_following2_columns',
'Wind_speed_max','Wind_speed_average','Quality_of_following12_columns','rain',
 'type_of_rain','sunny_hours','snow_height',
 'Average fraction of sky covered by clouds','steam_pressure_average','Air_pressure_average',
 'Air_temperature_average','relative_humidity_daily_average','Air_temp_max_2m','Air_temp_min_2m',
 'Air_temp_5cm']
    return merged_clean
