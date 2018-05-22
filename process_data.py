import numpy as np
import pandas as pd
import os
import glob


def process_data(userpath,stationnumber,time_interval):
    #function for database group to call
    if time_interval=='daily':
        merged = merge_hisrec_daily(userpath,stationnumber)
    elif time_interval=='hourly':
        merged = merge_hisrec_hourly(userpath,stationnumber)
    return clean_merged(merged)

def merge_hisrec_daily(userpath,stationnumber):
    histpath = os.path.join(userpath, 'pub','CDC','observations_germany','climate','daily','kl','historical')
    recpath  = os.path.join(userpath, 'pub','CDC','observations_germany','climate','daily','kl','recent')

    histfile_tmp = os.path.join(histpath, "produkt_klima_tag_*")
    histfile_tmp += str(stationnumber).zfill(5)+'.txt'
    histfile = glob.glob(histfile_tmp)[0]

    recfile_tmp = os.path.join(recpath, "produkt_klima_tag_*")
    recfile_tmp += str(stationnumber).zfill(5)+'.txt'

    histdata = pd.read_table(histfile, sep=";", low_memory=False)

    recfile_list = glob.glob(recfile_tmp)

    if recfile_list:

        recfile = glob.glob(recfile_tmp)[0]
        recentdata = pd.read_table(recfile, sep=";", low_memory=False)
        merged=pd.concat([histdata,recentdata])

    else:

        merged = histdata
                
    return merged

def clean_merged(merged):
    merged_clean = merged.replace(-999, np.nan, regex=True)
    merged_clean = merged_clean.drop(['eor'],axis=1)
    merged_clean.columns = [c.lower() for c in merged_clean.columns]
    merged_clean['mess_datum'] = pd.to_datetime(merged_clean['mess_datum'].apply(str))
    merged_clean = merged_clean.drop_duplicates()

    return merged_clean
