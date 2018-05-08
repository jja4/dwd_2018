from ftplib import FTP
import numpy as np
import codecs

server = "ftp-cdc.dwd.de"

def get_station_names():

    ftp = FTP(server)
    ftp.login()

    # Create a file stations.txt with all the station information
    filename = "pub/CDC/observations_germany/climate/daily/kl/historical/KL_Tageswerte_Beschreibung_Stationen.txt"
    file = open("stations.txt", 'wb')
    ftp.retrbinary('RETR '+ filename, file.write)
    file.close()

    x = codecs.open("stations.txt")
    print(x)

get_station_names()
