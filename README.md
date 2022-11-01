# zeversolar
## Read data from Zeversolar inverter

Zeversolar inverter can be reached within the network through (http://yourIPaddresshere/home.cgi)
The response it returns looks like my example:
  
1 1 xxxx yyyy M11 zzzz 14:21 29/10/2022 0 1 xyz 362 1.12 OK Error

The string shows the hardware names, date and time, the current energy production in Watts, the cumulative production in kWh and the status
  
The Python program does the following for ever:
- opens the URL to get the inverter string
  - if there is a '200' response
    - parse the string and get the interesting parts
    - store the fields in a Sqlite table
    - go to sleep for 5 minutes
  - else on error
    - go to sleep for 60 minutes
  
## Database SQLite3
### table ***eproduce***
Fields:
- **timestamp**    = local timestamp
- **inverter**     = hardware name
- **pac**          = energy produced in watts
- **cum**          = cumulative per day up to timestamp, tweaked it to decimal with comma use
- **status**       = as given by zeversolar, 0 is all fine
- **solar_stat**   = as given by zeversolar, OK is all fine
- **time_dat**     = timestamp of zeversolar measurement, in my case (after configuring inverter) same as local
- **urlstat**      = 200 (response received), 500 (inverter switched off)
