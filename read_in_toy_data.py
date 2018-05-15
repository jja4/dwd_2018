import numpy as np
import folium
import webbrowser
import os
from ftplib import FTP
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster

class Station:
    def __init__(self, id, von, bis, height, geobr, geola, name, land):
        self.id = id
        self.von = von
        self.bis = bis
        self.height = height
        self.geobr = geobr
        self.geola = geola
        self.name = name
        self.land = land
    def get_GPS(self):
        return np.array([self.geobr, self.geola]).astype('float')

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
        dict[Stations[line_vec[0]].id] = Stations[line_vec[0]].name
print("number of stations loaded: ",len(Stations))
fileorigin.close()

print(dict)
