#!/usr/bin/python3

##
## sml_reader.py     - reads sml data from smart meter
##                   - writes values as json to stdout
##
## This script was inspired by code and examples on volkszaehler.org [1].
## Thanks to all who contribute to this project. Using this script, I read
## sml data from an EDL21 eHZ smart meter [2] and use the resulting json
## to feed two databases with separate scripts. Connection to smart meter
## is realized by raspi and simple IR reader [3], using pySerial [4] to
## read data.
##
## Attention: make sure the executing user is a member of the group
##            'dialout' otherwise access to serial devive may be denied!
##
## sample output:
## { "data": {
##        "1.8.0": 10567470.0,
##        "16.7.0": -1565.1,
##        "2.8.0": 35836784.0
##    },
##    "sml_len": 396,
##    "sml_raw": "1B1B1B1B01010.....1CD1A013EB6"
## }
## [1] https://www.volkszaehler.org/
## [2] https://wiki.volkszaehler.org/hardware/channels/meters/power/edl-ehz/edl21-ehz
## [3] https://wiki.volkszaehler.org/howto/simpler_ir_leser
## [4] https://pyserial.readthedocs.io/en/latest/shortintro.html

##==== license section ========
## This code is under MIT License: Copyright (C) 2019 Bernd Künnen 
## License details see https://choosealicense.com/licenses/mit/

import sys
import json
import serial
import binascii as hex

##==== config section ========

# define serial parameters for your smart meter reader
ser_device  = '/dev/ttyS0'
ser_rate    =  9600
ser_timeout =  1
ser_maxloop =  7

# - usually you only need 1.8.0 and maybe are interested in 16.7.0
# - 2.8.0 is only relevant if you generate power, e.g. by photovoltaics
# - if in doubt keep all; 2.8.0 will be NULL if not existent
config = { 
  '1.8.0':  {'key':'070100010800FF', 'pos':20, 'len':10, 'comment': 'Strombezug aus dem Netz' }, 
  '2.8.0':  {'key':'070100020800FF', 'pos':20, 'len':10, 'comment': 'Stromeinspeisung in das Netz' }, 
  '16.7.0': {'key':'070100100700FF', 'pos':14, 'len':8,  'comment': 'Aktuelle Wirkleistung' }  
}

##==== code section ========

# function to decode sml data
def twos_complement(hexstr,bits):
  value = int(hexstr,16)
  if value & (1 << (bits-1)):
    value -= 1 << bits
  return value

##-- main() --
sml_num_bytes = 0
sml_num_loops = 0
while (sml_num_bytes < 300) and (sml_num_loops < ser_maxloop) :
  sml_num_loops += 1
  with serial.Serial(ser_device, ser_rate, timeout=ser_timeout) as ser: 	# 9600/8N1
    sml = ser.read(540)       					# read up to ten bytes (timeout)
  ser.close
  sml_num_bytes = len(sml)

# maybe the sensor broke or something else went wrong?
if sml_num_loops == ser_maxloop:
  sys.stderr.write('!! tried to read data from ' + ser_device + ' ' + str(ser_maxloop) + ' times, but received no data\n')
  sys.exit(3)

# convert binary sml sauce to hex string
sml_hex = hex.hexlify(sml).decode("utf-8").upper()

# create basic output json record
json_out = {}
json_out['sml_hex_bytes'] = sml_hex
json_out['sml_num_bytes'] = sml_num_bytes
json_out['sml_num_loops'] = sml_num_loops
json_out['data']    = {}

# read values from raw sml data
for obis in config.keys():
  pos1 = sml_hex.find( config[obis]['key'] )
  if pos1 < 0:
    # obis not found
    json_out['data'][obis] = null
  else:
    # found obis; add value to json
    offset = pos1+len(config[obis]['key'])
    start  = config[obis]['pos']
    stop   = config[obis]['pos'] + config[obis]['len']
    json_out['data'][obis] = twos_complement(sml_hex[offset:][start:stop], 32) / 10

# finally, write json record to stdout
print( json.dumps(json_out, indent=4, sort_keys=True) )

