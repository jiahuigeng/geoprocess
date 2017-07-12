# -*- coding: utf-8 -*-
"""
This is a module showing how to read csv-files.

@author: schwerjo
"""

import os
import csv

# Pfade vorbereiten (an eigene Ordnerstruktur anzupassen)
dir_script = os.path.abspath(os.path.dirname(__file__))
print dir_script

dir_data = os.path.join(dir_script, "data")
print dir_data

f_airports = os.path.join(dir_data, "of", "airports-extended.dat")
print f_airports

# csv Reader: Zeilen als Listen
with open(f_airports) as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        #print row
        pass

# csv DictReader: Zeilen als Dictionaries
with open(f_airports) as csvfile:
    fieldnames = ["airport_ID", "name", "city", "country", "iata", "icao",
              "lat", "lon", "alt", "tz", "dst", "dtz", "type", "src"]
    data = csv.DictReader(csvfile, fieldnames)
    for row in data:
        print row
        #print row["type"] # rows jetzt dictionaries