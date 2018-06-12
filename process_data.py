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

    histfile_tmp = os.path.join(histpath, "produkt_klima_tag_*") #list of filenames
    histfile_tmp += str(stationnumber).zfill(5)+'.txt'
    histlist = glob.glob(histfile_tmp)
    if histlist:
        histfile = glob.glob(histfile_tmp)[0]
        histdata = pd.read_table(histfile, sep=";", low_memory=False)
    else:
        histdata = []

    recfile_tmp = os.path.join(recpath, "produkt_klima_tag_*")
    recfile_tmp += str(stationnumber).zfill(5)+'.txt'
    reclist = glob.glob(recfile_tmp)
    if reclist:
        recfile = glob.glob(recfile_tmp)[0]
        recentdata = pd.read_table(recfile, sep=";", low_memory=False)
    else:
        recentdata = []

    merged=pd.concat([histdata,recentdata])

    return merged

def merge_hisrec_hourly(userpath,stationnumber):
    hour_folders = ["air_temperature", "cloud_type", "precipitation", "pressure", "soil_temperature", "solar", "sun", "visibility", "wind"]

    for i,folder in enumerate(hour_folders):
        histpath = os.path.join(userpath, 'pub','CDC','observations_germany','climate','hourly', folder, 'historical')
        recpath  = os.path.join(userpath, 'pub','CDC','observations_germany','climate','hourly', folder, 'recent')

        histfile_tmp = os.path.join(histpath, "stundenwerte*")
        histfile_tmp += str(stationnumber).zfill(5)+'*/produkt*'
        histlist = glob.glob(histfile_tmp)
        if histlist:
            histfile = glob.glob(histfile_tmp)[0]
            histdata = pd.read_table(histfile, sep=";", low_memory=False)
        else:
            histdata = []


        recfile_tmp = os.path.join(recpath, "stundenwerte*")
        recfile_tmp += str(stationnumber).zfill(5)+'*/produkt*'
        reclist = glob.glob(recfile_tmp)
        if reclist:
            recfile = glob.glob(recfile_tmp)[0]
            recentdata = pd.read_table(recfile, sep=";", low_memory=False)
        else:
            recentdata = []

        if i==0:
            merged_all=pd.concat([histdata,recentdata])
        if i>1:
            merged=pd.concat([histdata,recentdata])
            if merged['MESS_DATUM'] == merged_all['MESS_DATUM']:
                merged_all=pd.concat([merged_all,merged.drop(columns=['MESS_DATUM','STATIONS_ID','eor'])],axis=1)

    return merged_all

def clean_merged(merged):
    merged_clean = merged.replace(-999, np.nan, regex=True)
    merged_clean = merged_clean.drop(['eor'],axis=1)
    merged_clean.columns = [c.strip().lower() for c in merged_clean.columns]
    merged_clean['mess_datum'] = pd.to_datetime(merged_clean['mess_datum'].apply(str))
    merged_clean = merged_clean.drop_duplicates(subset = ['stations_id', 'mess_datum'], keep='first')
    merged_clean['mess_datum'] = merged_clean['mess_datum'].apply(lambda x: x.date())

    return merged_clean
