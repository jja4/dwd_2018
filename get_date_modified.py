
import pandas as pd
from urllib.request import urlopen

response = urlopen("ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/")
file = open("last_modified.txt", "wb")
data = response.read()
#print(data)
file.write(data)
file.close()

dat = open("last_modified.txt", "r")
#print(dat.read())

table = pd.read_table("last_modified.txt", delim_whitespace = True, header = 2)

#for i in range()
print(table)
