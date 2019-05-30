#!/usr/bin/python3

##
## write2vz.py   - reads json (generated by sml_reader.py) from stdin
##               - writes values to volkszaehler api
##
## Connect both scripts by pipe "sml_reader.py | write2vz.py" - and
## you're done. You need to configure the UUIDs from your volkszaehler
## instance below, and maybe the base url.
##

##==== license section ========
## This code is under MIT License: Copyright (C) 2019 Bernd Künnen 
## License details see https://choosealicense.com/licenses/mit/


##==== config section ====
# assign the uuids from your vz here
config = {
  "1.8.0":  "4dfbe7c0-2249-11e9-9631-53cb0a06555d",
  "2.8.0":  "66d03d60-2249-11e9-936d-73cbc07b6b8e",
  "16.7.0": "8c78f3b0-2249-11e9-acf8-ebb28fb5640b",
}

# base url of your vz installation - keep default when using vz image
vzbase = "http://localhost/middleware.php/data/"


##==== code section == no need to change lines below ====
import json, sys, requests

# load json from stdin
try:
  myjson = json.load(sys.stdin)
except:
  sys.stderr.write('!! error loading json')
  exit(1)

# decode json
try:
  for obis in myjson['data']:
    uuid  = config[obis]
    value = myjson['data'][obis]
    vzurl = vzbase + uuid + '.json?value=' + str(value)

    # write data to volkszaehler
    r = requests.post( vzurl, data={} )
    if r.status_code != 200:
      sys.stderr.write('!! error on writing to vz; url=' +  vzurl + ', http status=' + str(r.status_code) )

# catch if input is no valid json
except:
  sys.stderr.write('!!error: no data block in json')
  exit(2)

