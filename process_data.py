import numpy as np
import pandas as pd
import os
import glob

stationnumber = 44

userpath = "C:\\Users\\PCP2018\\Documents\\WeatherProject\\dwd_2018"

histpath = os.path.join(userpath, "pub\CDC\observations_germany\climate\daily\kl\historical")
recpath  = os.path.join(userpath, "pub\CDC\observations_germany\climate\daily\kl\\recent")

histfile_tmp = os.path.join(histpath, "produkt_klima_tag_*")
histfile_tmp += str(stationnumber).zfill(5)+'.txt'
histfile = glob.glob(histfile_tmp)[0]

recfile_tmp = os.path.join(recpath, "produkt_klima_tag_*")
recfile_tmp += str(stationnumber).zfill(5)+'.txt'
recfile = glob.glob(recfile_tmp)[0]
