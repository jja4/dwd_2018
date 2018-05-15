import os
import sys
from useftp import download_data
from unzip_all import unzip_folder

def get_data(userpath):
    #download the files
    print("getting data")
    download_data(userpath)

    #unzip the files
    print("unzipping data")
    localdir = os.path.join(userpath,'pub','CDC','observations_germany','climate','daily','kl')
    unzip_folder(os.path.join(localdir, 'historical'))
    unzip_folder(os.path.join(localdir, 'recent'))
    hour_folders = ["air_temperature", "cloud_type", "precipitation", "pressure", "soil_temperature", "sun", "visibility", "wind"]
    for folder in hour_folders:
        localdir = os.path.join(userpath, 'pub','CDC','observations_germany','climate','hourly', folder)
        if folder!="solar":
            unzip_folder(os.path.join(localdir, 'historical'))
            unzip_folder(os.path.join(localdir, 'recent'))
        else:
            unzip_folder(local_dir)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("get_data has 1 parameter: path to the folder, where the data will be downloaded")
        print("----------python get_data.py your_path")
    else:
        command = sys.argv[1]
        print(command)
        get_data(command)
