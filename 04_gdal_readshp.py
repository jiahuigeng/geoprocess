# -*- coding: utf-8 -*-
"""
This is a module showing how to read a shapefile and iterate over features.

@author: schwerjo
"""

import os


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

#Datenverzeichnis relativ zum Skript
dir_data = os.path.join(dir_script)
print dir_data

# Shapefile, das gelesen werden soll.
shp_countries = os.path.join(dir_data, "ne_10m_admin_0_countries",
                             "ne_10m_admin_0_countries.shp")

# Shp lesen: Driver spezifizieren

# GDAL-Shapefile-Driver: Mit welchem Dateityp haben wir es zu tun?
driver = ogr.GetDriverByName("ESRI Shapefile")

# DataSource-Objekt liefert Zugriff auf Datenquelle
# Shapefile-DataSource kann Verzeichnis mit mehreren Shapefiles sein.
# Argument zwei regel Schreibzugriff: 0 = Lesen, 1 = Lesen und Schreiben.
countries = driver.Open(shp_countries,0)

# Konnte auf die DataSource zugegriffen werden?
if countries is None:
    print "Kann nicht oeffnen!"

else:
    print "Funktioniert!"

    # Informationen zum Shapefile (vgl. ArcGIS arcpy "Describe"-Objekt)
    layer = countries.GetLayer() # Layer ist ein konkretes Shapefile der DataSource.

    print layer.GetFeatureCount() # Anzahl Features
    print layer.GetGeomType() # Numerischer Code des Geometrietyps
    print layer.GetExtent() # Ausmasse

    defn = layer.GetLayerDefn() # Layer-Definition: Attributfelder etc.

    print "Name  -  Type  Width  Precision"
    for i in range(defn.GetFieldCount()):
        fieldName =  defn.GetFieldDefn(i).GetName()
        fieldTypeCode = defn.GetFieldDefn(i).GetType()
        fieldType = defn.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
        fieldWidth = defn.GetFieldDefn(i).GetWidth()
        GetPrecision = defn.GetFieldDefn(i).GetPrecision()

        print fieldName + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision)

    # Durch alle Features iterieren
    for feature in layer:
        print feature.GetField("NAME")

    layer.ResetReading() # Zeiger auf erster Feature zuruecksetzen


    # Iterieren mit Attributfilter
    layer.SetAttributeFilter("POP_EST < 5000000")

    for feature in layer:
        name = feature.GetField("NAME")
        pop_est = feature.GetField("POP_EST")
        geom = feature.GetGeometryRef() #als WKT
        area = geom.GetArea() # Macht das Sinn bei WGS1984?
        print name, pop_est, area, geom
    layer.ResetReading()
    layer.SetAttributeFilter("") # Attributfilter zuruecksetzen. Bleibt ansonsten fuer "layer" bestehen.
