# -*- coding: utf-8 -*-
"""
Dieses Modul zeigt wie Kommandozeilen-Programme/-Befehle aus Python heraus
ausgefuehrt werden koennen. Dafuer gibt es das built-in Modul "subprocess".

Verdeutlichung anhand ogr2ogr.exe. Das ist ein Hilfsprogramm von OGR/GDAL, mit
dem unter anderem Reprojektionen und Transformationen durchgefuehrt werden koennen.

http://www.gdal.org/ogr2ogr.html


@author: schwerjo
"""

import os
import subprocess

# Test, ob GDAL-Komponenten importiert werden koennen
try:
    from osgeo import ogr, osr, gdal

    # Version aktuell genug?
    version_num = int(gdal.VersionInfo("VERSION_NUM"))
    print "GDAL Version", version_num
    if version_num < 1100000:
        raise Warning("ERROR: Python bindings of GDAL 1.10 or later required")
    # GDAL/OGR exceptions aktivieren
    gdal.UseExceptions()

except ImportError as e:
    raise SystemExit("ERROR: cannot import GDAL/OGR modules.\n{0}".format(e))

# Pfade vorbereiten (an eigene Ordnerstruktur anzupassen)
# Verzeichnis dieses Skriptes
dir_script = os.path.abspath(os.path.dirname(__file__))
print dir_script

# Datenverzeichnis
dir_data = os.path.join(dir_script, "data")
print dir_data


# subprocess
# Kommandozeilen-Befehle von Python aus ausfuehren

# Eckert IV-Projektion als proj.4-String:
#http://spatialreference.org/ref/esri/54012/proj4/
# WGS84 Eckert IV (flaechentreu) proj.4 "+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"

# Ein Kommandozeilenbefehl kann flexibel als Liste der Parameter konstruiert werden.
# subprocess setzt die Listenelemente zu einem Befehlsstring zusammen.
# Wichtig ist die richtige Reihenfolge der Parameter, so wie das externe Programm diese erwartet:
# Bestandteile des Befehls [auszufuehrende datei, args, ausgabedatei, eingangsdatei]

# Mit ogr2ogr.exe die Projektion eines Shapefiles aendern
ogr2ogr = r"C:\Users\schwerjo\AppData\Local\Continuum\Anaconda2\envs\py2017\Library\bin\ogr2ogr.exe"  # an eigene Umgebung anpassen
ogr2ogr_func = "-t_srs" # -t_srs srs_def: Reproject/transform to this SRS (srs_def) on output
srs_def = "+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs" # srs_def: hier als proj.4-String
shp_in = os.path.join(dir_data, "of", "airports_GER.shp")
shp_out = os.path.join(dir_data, "of", "airports_GER_EckIV.shp") # Reprojiziertes Ausgabe-Shapefile

command = [ogr2ogr, ogr2ogr_func, srs_def, shp_out, shp_in] # Befehl zusammensetzen

# Evtl. Error falls shapefile schon existiert
try:
    subprocess.check_call(command) # Befehl ausfuehren

except subprocess.CalledProcessError as e:
    # Falls Fehler auftritt
    print e




