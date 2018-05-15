import numpy as np
import os
from ftplib import FTP
import pickle

def get_station_names():
    """ Return a dictonary containing the station ID's
    as keys and the list [Stations_id, von_datum, bis_datum, Stationshoehe,
    geoBreite, geoLaenge, Stationsname, Bundesland] as value.
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
    stations_dict = {}

    for lineid, line in enumerate(fileorigin):
        if lineid > 1:
            line_vec = list(filter(None,line.split(' ')))
            Stations[line_vec[0]] = Station(line_vec[0],line_vec[1], line_vec[2], line_vec[3],
                                line_vec[4], line_vec[5], line_vec[6:-1], line_vec[-1])
            stations_dict[Stations[line_vec[0]].Stations_id] = [Stations[line_vec[0]].von_datum,
            Stations[line_vec[0]].bis_datum, Stations[line_vec[0]].Stationshoehe,
            Stations[line_vec[0]].geoBreite, Stations[line_vec[0]].geoLaenge,
            Stations[line_vec[0]].Stationsname, Stations[line_vec[0]].Bundesland]
    print("number of stations loaded: ",len(Stations))
    fileorigin.close()

    # Join town names that are made up of multiple strings
    for key in stations_dict:
        if len(stations_dict[key][5]) > 2:
            town_name = stations_dict[key][5][0:-1]
            land_name = stations_dict[key][5][-1]
            joint_name = " ".join(town_name)
            stations_dict[key][5] = joint_name
            stations_dict[key][6] = land_name
        else:
            stations_dict[key][6] = stations_dict[key][5][1]
            stations_dict[key][5] = stations_dict[key][5][0]

    return stations_dict


if __name__ == '__main__':
    stations_dict = get_station_names()
    pickle.dump(stations_dict, open("stations.p", "wb"))
