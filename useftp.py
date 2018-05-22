from ftplib import FTP
import os, sys

server = "ftp-cdc.dwd.de"

def download_folder(ftp, userpath,foldername, VERBOSE = True):
    filenames = ftp.nlst(foldername)
    k = 0 #percentage downloade counter
    for i, filename in enumerate(filenames):
        local_filename = os.path.join(userpath, filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR '+ filename, file.write)
        file.close()
        if VERBOSE:
            # what this actually does is to overwrite the last printout that was the statusbar
            # the ljust method pads the string with whitespaces, this is needed to remove
            # the previous statusbar
            sys.stdout.write("downloaded {}".format(filename).ljust(200))
            sys.stdout.write('\n')
            sys.stdout.flush()
        sys.stdout.write("[{}{}] {}%\r".format('='*k,' '*(101-k), k))
        sys.stdout.flush()
        if i%int(len(filenames)/100)==0: #update status every 1%
            k+=1

def delete_folder(folder, VERBOSE = True):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
            os.unlink(file_path)
            if VERBOSE:
                print("deleted contents of folder "+folder)
        except Exception as e:
            print(e)

def download_data(userpath, historical=True, recent=True, hourly=True, VERBOSE = True):
    ftp = FTP(server)
    ftp.login()
    if VERBOSE: print("logged in to server {}".format(server))
    if historical:
        if VERBOSE: print("gonna get historical data")
        get_historical_data(userpath)
    if recent:
        if VERBOSE: print("gonna get recent data")
        get_recent_data(userpath)
    if hourly:
        if VERBOSE: print("gonna get hourly data")
        get_hourly_data(userpath)

def get_historical_data(userpath,VERBOSE=True):
    histpath = os.path.join(userpath,'pub/CDC/observations_germany/climate/daily/kl/historical/')
    if VERBOSE: print('directory for historical data: {}'.format(histpath))
    if not os.path.isdir(histpath):
        if VERBOSE: print("directory did not exist, it will be created")
        os.makedirs(histpath)
        download_folder(ftp, userpath,'pub/CDC//observations_germany/climate/daily/kl/historical', VERBOSE=VERBOSE)

def get_recent_data(userpath,VERBOSE=True):
    recentpath = os.path.join(userpath,'pub/CDC/observations_germany/climate/daily/kl/recent/')
    if VERBOSE: print("directory for recent data: {}".format(recentpath))
    if not os.path.isdir(recentpath):
        if VERBOSE: print("directory did not exist, it will be created")
        os.makedirs(recentpath)
    else:
        if VERBOSE: print("deleting previous version of recent data")
        delete_folder(recentpath, VERBOSE = True)

    download_folder(ftp, userpath, 'pub/CDC//observations_germany/climate/daily/kl/recent',VERBOSE=VERBOSE)

def get_hourly_data(userpath,VERBOSE=True):
    hour_folders = ["air_temperature", "cloud_type", "precipitation", "pressure", "soil_temperature", "sun", "visibility", "wind"]
    if VERBOSE: print("will now download hourly predictions")
    for folder in hour_folders:
        if VERBOSE: print("now downloading {}".format(folder))
        hourpath = os.path.join('pub/CDC//observations_germany/climate/hourly/', folder)
        if VERBOSE: print("the data will be saved in {}".format(hourpath))
        hourpath_hist = os.path.join(userpath, hourpath, 'historical')
        hourpath_recent = os.path.join(userpath, hourpath, 'recent')

        if not os.path.isdir(hourpath_hist):
            if VERBOSE: print("downloading historical hourly data")
            os.makedirs(hourpath_hist)
            download_folder(ftp, userpath, hourpath+'/historical',VERBOSE=VERBOSE)

        if not os.path.isdir(hourpath_recent):
            if VERBOSE: print("downloading recent hourly data")
            os.makedirs(hourpath_recent)
        else:
            if VERBOSE: print("deleting previous version of recent data")
            delete_folder(hourpath_recent, VERBOSE = True)

        download_folder(ftp, userpath, hourpath+'/recent',VERBOSE=VERBOSE)

    solarpath = 'pub/CDC//observations_germany/climate/hourly/solar'
    if VERBOSE: print("now downloading solar hourly data into {}".format(solarpath))
    if not os.path.isdir(solarpath):
        os.makedirs(solarpath)
    else:
        if VERBOSE: print("deleting previous version of solar data")
        delete_folder(solarpath, VERBOSE = True)
    download_folder(ftp, userpath, solarpath,VERBOSE=VERBOSE)
