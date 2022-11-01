############################################################################################
# By:       Jos
# Date:     Nov 2022
# Function: get produced solar energy levels from ZeverSloar Inverter
############################################################################################
# Version : 0.91
############################################################################################

import urllib.request
from urllib.error import URLError, HTTPError

import sqlite3
import time
import datetime
import pytz
import decimal

# use right time zone
UTC = pytz.utc
CET = pytz.timezone('Europe/Amsterdam')

# Configure SQLite database
con = sqlite3.connect("stillhaveit.db", check_same_thread=False) 
print ("Opened database successfully")

# URL for inverter within WiFi network
myUrl = "http://192.168.178.82/home.cgi"

# set timer to sleep for 5 minutes
t = 300

# loop every (t) seconds forever
while True:
    # open URL and check return code
    try:
        res = urllib.request.urlopen(myUrl)
    except URLError:
        mycode = "500"
        myustatus = "Inverter switched off!"
        print("code: " + mycode + " status: " + myustatus)
        
        # no response
        mytimestamp = datetime.datetime.now(CET)
        myurlstat = mycode + "/" + myustatus    
        myinverter = ""
        mytime_dat = ""
        mystatus = ""
        mypac = "0" 
        mycum = "0" 
        mysolar_stat = "OFF"
        # try again over an hour
        t = 3600
        
    else:
        t = 300
        mycode = "200"
        myustatus = ""
        # response is parsed from inverter string
        mytimestamp = datetime.datetime.now(CET)
        myurlstat = mycode + "/" + myustatus    
        strres = res.read(300).decode('utf-8')
        
        x = strres.split('\n', 13)
        myinverter = x[2]
        mytime_dat = x[6] 
        mystatus = x[7]
        mypac = x[10]
        mycum = x[11]
        # zeversolar is incorrect with decimals so I have to correct it
        mycumd = decimal.Decimal(mycum)
        if mycumd < 1 and len(mycum) == 3:
            mycum = mycum[:2] + "0" + mycum[2:]
        mycum = mycum.replace(".", "," )   # decimal comma for local (dutch) usage
        mysolar_stat = x[12]
    
    # response is stored within database
    con.execute(
        "INSERT INTO eproduce (timestamp, inverter, pac, cum, status, solar_stat, time_dat, urlstat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (            
        str(mytimestamp),
        myinverter,
        mypac,
        mycum,
        mystatus,
        mysolar_stat,
        mytime_dat,
        myurlstat
        )
    ) 
    con.commit()

    # loop sleeps for 300 sec  
    print("Going to sleep for " + str(t) + " seconds now.")  
    time.sleep(t)
