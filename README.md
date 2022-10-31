# zeversolar
## Read data from Zeversolar inverter

Zeversolar inverter can be reached within the network through http://<your IP address>/home.cgi
The response it returns looks like my example:
  
1 1 xxxx yyyy M11 zzzz 14:21 29/10/2022 0 1 xyz 362 1.12 OK Error

The string shows the hardware names, date and time, the current energy production in Watts, the cumulative in Kwh and the status
  
The Python program does the following for ever:
-opens the URL to get the inverter string
 -if there is a '200' response
  -parse the string and get the interesting parts
  -store the fields in a Sqlite table
  -go to sleep for 5 minutes
 -else on error
  -go to sleep for 60 minutes
  
