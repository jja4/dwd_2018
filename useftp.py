from ftplib import FTP
import os

server = "ftp-cdc.dwd.de"
serverpath = "/pub/CDC/observations_germany/climate/hourly"

ftp = FTP(server)
ftp.login()


filenames = ftp.nlst('pub/CDC//observations_germany/climate/daily/kl/historical')
os.makedirs('/Users/pcp/test/pub/CDC/observations_germany/climate/daily/kl/historical/')


for filename in filenames:
    local_filename = os.path.join('/Users/pcp/test', filename)
    file = open(local_filename, 'wb')
    ftp.retrbinary('RETR '+ filename, file.write)
    file.close()
