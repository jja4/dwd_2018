from ftplib import FTP
import os

server = "ftp-cdc.dwd.de"

def download_folder(ftp, userpath,foldername):
    filenames = ftp.nlst(foldername)
    for filename in filenames:
            local_filename = os.path.join(userpath, filename)
            file = open(local_filename, 'wb')
            ftp.retrbinary('RETR '+ filename, file.write)
            file.close()


def download_data(userpath):

    ftp = FTP(server)
    ftp.login()

    # get historical data, if it isn't already stored
    histpath = os.path.join(userpath,'pub/CDC/observations_germany/climate/daily/kl/historical/')
    if not os.path.isdir(histpath):
        os.makedirs(histpath)
        download_folder(ftp, userpath,'pub/CDC//observations_germany/climate/daily/kl/historical')

    # get recent data
    recentpath = os.path.join(userpath,'pub/CDC/observations_germany/climate/daily/kl/recent/')
    if not os.path.isdir(recentpath):
        os.makedirs(recentpath)
    download_folder(ftp, userpath, 'pub/CDC//observations_germany/climate/daily/kl/recent')

    # get hourly data
    hour_folders = ["air_temperature", "cloud_type", "precipitation", "pressure", "soil_temperature", "sun", "visibility", "wind"]
    for folder in hour_folders:
        hourpath = os.path.join('pub/CDC//observations_germany/climate/hourly/', folder)
        print(hourpath)
        hourpath_hist = os.path.join(userpath, hourpath, 'historical')
        hourpath_recent = os.path.join(userpath, hourpath, 'recent')

        if not os.path.isdir(hourpath_hist):
            os.makedirs(hourpath_hist)
            download_folder(ftp, userpath, hourpath+'/historical')

        if not os.path.isdir(hourpath_recent):
            os.makedirs(hourpath_recent)
        download_folder(ftp, userpath, hourpath+'/recent')

    solarpath = 'pub/CDC//observations_germany/climate/hourly/solar'
    if not os.path.isdir(solarpath)
        os.makedirs(solarpath)
    download_folder(ftp, userpath, solarpath)
