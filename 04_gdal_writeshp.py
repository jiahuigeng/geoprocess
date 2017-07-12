# -*- coding: utf-8 -*-
"""
This is a module showing ho to write to a shapefile.

!!!
Falls Ihr erzeugtes Shapefile keine oder eine leere Projektionsdatei (*.prj) hat:
GDAL_DATA Umgebungsvariable korrekt gesetzt? Scheinbar in manchen Versionen ein Anaconda-Problem:
https://github.com/conda-forge/gdal-feedstock/issues/54

Setzen Sie eine Umgebungsvariable "GDAL_DATA" mit dem Pfad zum Data-Verzeichnis von GDAL.
Dieses Verzeichnis enthält u.a. die Dateien "gcs.csv" und "epsg.wkt".
Fuer eine Anaconda-Environment ist der Wert von GDAL_DATA z.B.:
C:\Users\schwerjo\AppData\Local\Continuum\Anaconda2\envs\py2017\Library\share\gdal
!!!

@author: schwerjo
"""

import os
import csv


# Test, ob GDAL-Komponenten importiert werden koennen
try:
    from osgeo import ogr, osr, gdal

    # Version aktuell genug?
    version_num = int(gdal.VersionInfo('VERSION_NUM'))
    print "GDAL Version", version_num
    if version_num < 1100000:
        raise Warning('ERROR: Python bindings of GDAL 1.10 or later required')
    # GDAL/OGR exceptions aktivieren
    gdal.UseExceptions()

except ImportError as e:
    raise SystemExit('ERROR: cannot import GDAL/OGR modules.\n{0}'.format(e))

# Pfade vorbereiten (an eigene Ordnerstruktur anzupassen)
# Verzeichnis dieses Skriptes
dir_script = os.path.abspath(os.path.dirname(__file__))
print dir_script

# Datenverzeichnis
dir_data = os.path.join(dir_script)
print dir_data

# csv-Datei mit Airport Daten
f_airports = os.path.join(dir_data, "airports.dat")
print f_airports

# Shapefile, das geschrieben werden soll
shp_gdal = os.path.join(dir_data, "airports.shp")


# GDAL-Shapefile-Driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# Eventuell existierenden Shapefile loeschen und neu erstellen.
if os.path.exists(shp_gdal): #Alternative: os.path.isfile(shp_gdal):
    driver.DeleteDataSource(shp_gdal)
shp = driver.CreateDataSource(shp_gdal)

# Spatial Reference des Shapefiles definieren
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326) # EPSG:4326 ist WGS1984

# Layer anlegen: Soll Punkt-Geometrien enthalten.
layer = shp.CreateLayer("layer", srs, ogr.wkbPoint)

# Attributfelder des Layers und deren Datentypen definieren
field_id = ogr.FieldDefn("airport_ID", ogr.OFTInteger) # Feld definieren
layer.CreateField(field_id) # Feld erstellen
field_name = ogr.FieldDefn("name", ogr.OFTString)
layer.CreateField(field_name)
field_lat = ogr.FieldDefn("lat", ogr.OFTReal)
layer.CreateField(field_lat)
field_lon = ogr.FieldDefn("lon", ogr.OFTReal)
layer.CreateField(field_lon)

# Durch csv-Zeilen iterieren, Feature pro Zeile erzeugen und in Shapefile schreiben
with open(f_airports) as csvfile:
    fieldnames = ["airport_ID", "name", "city", "country", "iata", "icao",
              "lat", "lon", "alt", "tz", "dst", "dtz", "type", "src"]
    data = csv.DictReader(csvfile, fieldnames)
    for row in data:
        # Feature anlegen und Werte aus csv in shp-Attribute schreiben
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("airport_ID", row["airport_ID"])
        feature.SetField("name", row["name"])
        lat = float(row["lat"])
        lon = float(row["lon"])
        feature.SetField("lat", lat)
        feature.SetField("lon", lon)

        # Feature-Geometrie als Well-Known-Text aus den lat-/Lon-Strings erzeugen
        wkt = "POINT({0} {1})".format(lon, lat)
        point = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point)

        # Feature im Shapefile-Layer tatsaechlich erstellen
        layer.CreateFeature(feature)

        # GDAL-Objektreferenz manuell deallokieren, passiert bei GDAL wegen C++-Implementierung
        # leider nicht von selbst ueber Python Garbage Collector.
        # Ansonsten werden Features nicht geschrieben oder es gibt einen None-Type Fehler:
        del feature
del shp

