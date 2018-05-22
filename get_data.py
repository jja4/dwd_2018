#!/usr/bin/env python3

import os
import sys
from useftp import download_data
from unzip_all import unzip_folder
import getopt

def get_data(userpath, historical = True, recent = True, hourly = True, verbose = True):
    #download the files
    print("getting data")
    download_data(userpath = userpath,
                  historical = historical,
                  recent = recent,
                  hourly = hourly,
                  verbose = verbose)

    #unzip the files
    print("unzipping data")
    localdir = os.path.join(userpath,'pub','CDC','observations_germany','climate','daily','kl')
    unzip_folder(os.path.join(localdir, 'historical'))
    unzip_folder(os.path.join(localdir, 'recent'))
    hour_folders = ["air_temperature", "cloud_type", "precipitation", "pressure", "soil_temperature", "solar", "sun", "visibility", "wind"]
    for folder in hour_folders:
        localdir = os.path.join(userpath, 'pub','CDC','observations_germany','climate','hourly', folder)
        if folder!="solar":
            unzip_folder(os.path.join(localdir, 'historical'))
            unzip_folder(os.path.join(localdir, 'recent'))
        else:
            unzip_folder(localdir)


def main():
    try:
        options, args = getopt.getopt(sys.argv[1:], "vgrsh", ["verbose", "historical", "recent", "hourly","help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    verbose = False
    historical = False
    recent = False
    hourly = False
    help = False
    for opt, arg in options:
        if opt in ("-v", "--verbose"): verbose = True
        elif opt in ("-h", "--help"):
            help = True
            usage()
        elif opt in ("-g","--historical"): historical = True
        elif opt in ("-r", "--recent"): recent = True
        elif opt in ("-s","--hourly"): hourly = True
        else: assert False, "unhandled option"

    try: path = args[0]
    except IndexError:
        if not help:
            print("Must provide a path.")
            usage()
        sys.exit(2)

    get_data(userpath = path,
             historical = historical,
             recent = recent,
             hourly = hourly,
             verbose = verbose)

def usage():
    print("""Usage: 'python get_data -vgrsh path'\n
    arguments:\n
    \t path : the path where you want to save the data \n
    options:\n
    \t -v/--verbose : verbose mode\n
    \t -g/--historical : download historical data\n
    \t -r/--recent : download recent data\n
    \t -s/--hourly : download recent and historical hourly data
    \t -h/--help
    """)

if __name__ == "__main__":
    main()
