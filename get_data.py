import os
import sys
from useftp import download_data
from unzip_all import unzip_folder

def get_data(usrpath):
    #download the files
    print("getting data")
    userpath = usrpath
    download_data(userpath)
    #os.system("./useftp.py userpath")

    #unzip the files
    localdir = os.path.join(userpath,'pub/CDC/observations_germany/climate/daily/kl/')
    unzip_folder(os.path.join(localdir, 'historical/'))
    unzip_folder(os.path.join(localdir, 'recent/'))
    #os.system("./unzip_all.py localdir")


if __name__ == '__main__':
    if len(sys.argv) == 1: 
        print("get_data has 1 parameter: path to the folder, where the data will be downloaded")
        print("----------python get_data.py your_path")
    else:
        command = sys.argv[1]
        print(command)
        get_data(command)
