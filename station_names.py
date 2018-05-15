import numpy as np
import os
from ftplib import FTP
import pickle

def get_station_names():
    """ This function produces a pickled dictonary containing the station ID's
    as keys and a list of ['town name', 'Bundesland name']
    """

    class Station:
        def __init__(self, Stations_id, von_datum, bis_datum, Stationshoehe,
        geoBreite, geoLaenge, Stationsname, Bundesland):
            self.Stations_id = Stations_id
            self.von_datum = von_datum
            self.bis_datum = bis_datum
            self.Stationshoehe = Stationshoehe
            self.geoBreite = geoBreite
            self.geoLaenge = geoLaenge
            self.Stationsname = Stationsname
            self.Bundesland = Bundesland


    # Download the file from the internet
    server = "ftp-cdc.dwd.de"
    ftp = FTP(server)
    ftp.login()

    # Create a file stations.txt with all the station information
    filename = "pub/CDC/observations_germany/climate/daily/kl/historical/KL_Tageswerte_Beschreibung_Stationen.txt"
    file = open("stations.txt", 'wb')
    ftp.retrbinary('RETR '+ filename, file.write)
    file.close()

    fileorigin = open("stations.txt", 'r', encoding = "cp1250")
    partial_read_in = False
    Stations = {}
    dict = {}

    for lineid, line in enumerate(fileorigin):
        if lineid > 1:
            line_vec = list(filter(None,line.split(' ')))
            Stations[line_vec[0]] = Station(line_vec[0],line_vec[1], line_vec[2], line_vec[3],
                                line_vec[4], line_vec[5], line_vec[6:-1], line_vec[-1])
            dict[Stations[line_vec[0]].Stations_id] = [Stations[line_vec[0]].von_datum,
            Stations[line_vec[0]].bis_datum, Stations[line_vec[0]].Stationshoehe,
            Stations[line_vec[0]].geoBreite, Stations[line_vec[0]].geoLaenge,
            Stations[line_vec[0]].Stationsname, Stations[line_vec[0]].Bundesland]
    print("number of stations loaded: ",len(Stations))
    fileorigin.close()

    # Join town names that are made up of multiple strings
    for key in dict:
        if len(dict[key][5]) > 2:
            town_name = dict[key][5][0:-1]
            land_name = dict[key][5][-1]
            joint_name = " ".join(town_name)
            dict[key][5] = joint_name
            dict[key][6] = land_name

    print(dict)
    pickle.dump(dict, open("stations.p", "wb"))

get_station_names()
