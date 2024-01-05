# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 09:26:18 2024

@author: Alois
"""

import requests
import json
import ftplib
import os
import datetime
import pytz

FTP_HOST = os.environ['FTP_HOST']
FTP_USER = os.environ['FTP_USER']
FTP_PASS = os.environ['FTP_PASS']

tz = pytz.timezone('Europe/Paris')
timestamp = datetime.datetime.now(tz).strftime("%d/%m/%Y-%H:%M:%S")

try :
    i = requests.get("https://www.insa-lyon.fr")
    i_code = i.status_code
except :
    i_code = 404
try :
    m = requests.get("https://moodle.insa-lyon.fr")
    m_code = m.status_code
except :
    m_code = 404

d = {timestamp: {"insa-lyon.fr": i_code, "moodle.insa-lyon.fr": m_code}}

# connect to the FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
# force UTF-8 encoding
ftp.encoding = "utf-8"

ftp.sendcmd('CWD htdocs/insadown/')

filename = "data.json"
# with open(filename, "wb") as file:
#     # use FTP's RETR command to download the file
#     ftp.retrbinary(f"RETR {filename}", file.write)

# with open(filename, 'r') as f :
#     old = json.load(f)
    
# new = {**old, **d}

with open(filename, 'w') as f :
    json.dump(d, f)


with open(filename, "rb") as file:
    # use FTP's STOR command to upload the file
    ftp.storbinary(f"STOR {filename}", file)