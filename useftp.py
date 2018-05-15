from ftplib import FTP
import os

server = "ftp-cdc.dwd.de"

def download_data(userpath):

    ftp = FTP(server)
    ftp.login()

    # get historical data, if it isn't already stored
    histpath = os.path.join(userpath,'pub/CDC/observations_germany/climate/daily/kl/historical/')
    if not os.path.isdir(histpath):
        filenames = ftp.nlst('pub/CDC//observations_germany/climate/daily/kl/historical')
        os.makedirs(histpath)

        for filename in filenames:
            local_filename = os.path.join(userpath, filename)
            file = open(local_filename, 'wb')
            ftp.retrbinary('RETR '+ filename, file.write)
            file.close()

    filenames = ftp.nlst('pub/CDC//observations_germany/climate/daily/kl/recent')
    
    if not os.path.isdir(os.path.join(userpath,'pub/CDC/observations_germany/climate/daily/kl/recent/')):
        os.makedirs(os.path.join(userpath,'pub/CDC/observations_germany/climate/daily/kl/recent/'))

    for filename in filenames:
        local_filename = os.path.join(userpath, filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR '+ filename, file.write)
        file.close()
