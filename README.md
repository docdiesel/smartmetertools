# smartmetertools
Some tools for reading data from smartmeters

## About
Modern smartmeters provide an IR serial interface on which they send
data in sml format, containing such data like current power and energy
consumption. I wanted to read data from my smartmeter and found
volkszaehler.org, which gave me a good start.

Later I started to write my own tools which are to be found here. In May
2019 it#s just a couple of python scripts which read the sml and convert it
to json, giving the possibility to write it to different destinations
easily.

## The scripts

* bin/sml_reader.py : reads the sml data from the smart meter and writes it as json to stdout.
* bin/write2cly.py : reads the json and writes data to InfluxDB on corlysis.com.
* bin/write2vz.py : reads the json and writes the data into a 'volkszaehler' installation

## Links

* https://volkszaehler.org/ - software to read and visualize data from your smartmeter, up to a complete raspi image. You'll find instructions how to build a sensor, too.
* https://wiki.volkszaehler.org/howto/simpler_ir_leser - simple IR SML sensor; works for me.


