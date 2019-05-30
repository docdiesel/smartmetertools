# smartmetertools
Einige Werkzeuge zum Auslesen von Daten aus einem Smartmeter

## Worum geht's?
Moderne Stromzähler (aka Smartmeter) besitzen eine IR-basierte serielle
Schnittstelle, über die sie Daten zu aktueller Wirkleistung und bisherigem
Energieverbrauch ausgeben. Diese Daten wollte ich aus meinem Zähler auslesen
und fand unter volkszaehler.org Software, die mir einen guten Start
ermöglichte.

Später schrieb ich meine eigenen Python-Skripte, welche die SML-daten nach
JSON konvertieren und so das Weiterverarbeiten und Speichern in verschiedenen Ziel-Systemen
vereinfachen.

## Die Skripte

* bin/sml_reader.py : liest die SML-Daten vom Zähler und gibt sie als Json auf stdout aus.
* bin/write2cly.py  : liest das Json aus und schreibt die Daten in eine InfluxDB auf corlysis.com.
* bin/write2vz.py   : liest das Json und schreibt die Daten in eine 'volkszaehler'-Instalation.

## Links

* https://volkszaehler.org/ - Software-Projekt, welches sich mit dem Auslesen und Visualisieren von Daten aus Smartmetern befasst, bis hin zum kompletten Raspi-Image. Hier finden sich auch einige Anleitungen zum Bauen eines IR-Lesekopfes.
* https://wiki.volkszaehler.org/howto/simpler_ir_leser - einfacher IR SML-Lesekopf; funktioniert bei mir.

