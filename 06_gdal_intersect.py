4# -*- coding: utf-8 -*-
"""
Modul, das die Anwendung geometrisch-topologischer Methoden mit OGR am Beispiel
Intersection (Ueberschneidung) zeigt.

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

# Datenverzeichnis
dir_data = os.path.join(dir_script)
print dir_data

# Shapefile, das geschrieben werden soll
shp_countries = os.path.join(dir_data, "ne_10m_admin_0_countries.shp")
shp_pplaces = os.path.join(dir_data, "ne_10m_populated_places.shp")

# Intersection von Populated Places mit Countries
# Welche Populated Places schneiden welche Laender?

driver = ogr.GetDriverByName("ESRI Shapefile")

# Datasources
pplaces = driver.Open(shp_pplaces, 0)
countries = driver.Open(shp_countries, 0)

# Layer
pplaces_layer = pplaces.GetLayer()
countries_layer = countries.GetLayer()

# Geometrien laden und in geschachtelten Schleifen auf Ueberschneidung testen.
# Schleifen sind teure Operationen, keine besonders effiziente Strategie.
# Zur Veranschaulichung aber ausreichend. Zur Beschleunigung z.B. Indizes verwenden.

# Iteriere alle Laender und teste, welche Populated Places schneiden
# Alternativ koennten wir auch die Places auf Ueberschneidung durch Countries testen,
# d.h. die Verschachtelung anders herum aufbauen.
for c in countries_layer:

	# Geometrie-Objekt
	c_geom = c.GetGeometryRef()

	# Welche Populated Places schneiden diese Laendergeometrie?
	for pp in pplaces_layer:

		# Geometrie-Objekt
		pp_geom = pp.GetGeometryRef()

		# Ueberschneidung pruefen
		# Intersects --> Boolean: Ueberschneidung True/False
		intersect = c_geom.Intersects(pp_geom)

		# Intersection --> Ueberschneidungs-Geometrie
		# None falls keine Ueberschneidung
		intersection = c_geom.Intersection(pp_geom)

		# Falls Intersects --> True
		if intersect:
			print c.GetField("NAME"), "-", pp.GetField("NAME")
			# print intersection
	# Layer-Iterator fuer naechsten Schleifendurchlauf wieder auf Anfang setzen
	pplaces_layer.ResetReading()

# Zu guter Letzt auch fuer Countries-Layer zuruecksetzen, falls wir nochmal auf
# diesen Layer zurueckgreifen sollten...
countries_layer.ResetReading()


















