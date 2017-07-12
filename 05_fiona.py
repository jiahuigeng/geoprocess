# -*- coding: utf-8 -*-
"""
Modul, das den grundlegenden Umgang mit fiona zeigt.

fiona ist ein python-Wrapper fuer GDAL, der einen Zugriff auf GDAL mit
nativen Python-Strukturen und -Datentypen ermoeglicht.

fiona Dokumentation:
http://toblerity.org/fiona/manual.html

Am Ende des Skriptes erfolgt eine Analyse auf Attributwerte und Geometrie-Filter:
Wie viele und welche Airports liegen in Deutschland?

@author: schwerjo
"""

import os
import fiona

# gdal importieren wir nur fuer die Funktion "delete_feature()"
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
dir_data = os.path.join(dir_script)
print dir_data

# csv-Datei mit Airport Daten
f_airports = os.path.join(dir_data, "airports.dat")
print f_airports

# Shapefile, das geschrieben werden soll
shp_gdal = os.path.join(dir_data, "airports.shp")


# Lesen und Beschreiben einer Datenquelle

def describe_shp(path):
    """
    Shapefile-Eigenschaften beschreiben:
    Ein paar exemplarische Infos zu einer fiona feature-collection.
    """
    with fiona.open(path) as c:

        print "Was enthaelt \'shp\' nach einlesen mit fiona: {}".format(c)  # fiona collection
        print "Ein paar Eigenschaften des Layers:"  # unary predicates
        print "shp fuer Zugriff geschlossen: {}".format(c.closed)  # False innerhalb "with"
        print "Welchen driver hat fiona fuer Datenquelle genutzt? {}".format(c.driver)
        print "Extent: {}".format(c.bounds)
        print "CRS: {}".format(c.crs)
        print "Schema (LayerDefinition bei GDAL): {}".format(c.schema)
        print "meta: ", c.meta
        print "meta.schema", c.meta["schema"]

#describe_shp(shp_gdal)


def describe_feature(feature):
    """
    features sind bei fiona dictionaries.
    """
    print "Feature mit FID {}: {}".format(feature["id"], feature["id"])
    print "keys: {}".format(feature.keys()) # dict keys

    # Die Geometrie des Features
    print "geometry: {}".format(feature["geometry"])
    # Die Attribute und deren Werte des Features
    print "properties: {}".format(feature["properties"])


# Iteration durch collection
with fiona.open(shp_gdal) as c: # collection

        for feature in c:
            # tu etwas mit features
            #describe_feature(feature)
            pass


def feature_count(path):
    """
    Anzahl features in fiona-collection.
    """
    with fiona.open(path) as c:
        return len(list(c))

print feature_count(shp_gdal)


def get_feature(shp, feature_id):
    """
    Ein bestimmtes Feature über dessen ID aus collection extrahieren.
    """
    with fiona.open(shp) as c:
        return c[feature_id]

#feature = get_feature(shp_gdal, 3333)
#print feature


# Features schreiben

# Einen Beispieldatensatz herausziehen und anhaengen

# Fiona Doc: A vector file can be opened for writing in mode 'a' (append) or mode 'w' (write).
# Fiona's output is buffered. The records passed to write() and writerecords()
# are flushed to disk when the collection is closed.
# You may also call flush() periodically to write the buffer contents to disk.
# File fuer 'append' ('a') oeffnen:

def append_feature(shp, feature):
    """
    feature arg:
    Multiple Features --> Liste [feature, feature, ...]
    Ein Feature --> Feature (Dictionary)
    """
    with fiona.open(shp, 'a') as c:

        if isinstance(feature, list):
            # Liste [feature, feature, feature] mit mehreren Features anhaengen
            c.writerecords(feature)
        elif isinstance(feature, dict):
            # Einzelnes Feature anhaengen, ein fiona-Feature ist einfach ein dictionary
            c.write(feature)

#append_feature(shp_gdal, feature) # haengt Feature am Ende des Shapefiles an.
print feature_count(shp_gdal) # Count jetzt um Eins hoeher


def delete_feature_from_shp(path, fid):
    """
    Feature ueber FID mit OGR aus shapefile loeschen.

    Fiona collections (sowie viele andere Bibliotheken/Treiber) unterstuetzen das nicht.
    Beachte, dass "REPACK" auf dbf-file des shapefiles noetig ist um das Loeschen
    tatsaechlich durchzufuehren.
    """
    # GDAL-Shapefile-Driver
    driver = ogr.GetDriverByName('ESRI Shapefile')
    # DataSource mit write-access
    source = driver.Open(path, 1)
    # Layer der DataSource
    layer = source.GetLayer()
    layer.DeleteFeature(int(fid))  # feature ueber FID als geloescht markieren
    # Loeschen in dbf-File des shapefiles tatsaechlich vollziehen
    source.ExecuteSQL("REPACK {}".format(layer.GetName()))
    del source

# Das zuvor angehaengte Feature wieder loeschen, ID abhaengig von Ihrer Umgebung.
#delete_feature_from_shp(shp_gdal, 7189)
#print feature_count(shp_gdal) # Count jetzt wieder um Eins niedriger


# Neues Shapefile erstellen (auf Basis eines bestehenden Shapefiles)
# Das Schema in fiona entspricht etwa der LayerDefinition in GDAL.
# Erstellung eines Shapefiles von Grund auf im Prinzip analog zu GDAL,
# siehe fiona Dokumentation.

def create_shp_from_shp(template_shp, shp):
    template = fiona.open(template_shp)
    # über kwarg **template.meta bekommen wir das Schema als Vorlage
    shp = fiona.open(shp, "w", **template.meta)
    template.close() # Hier .close() noetig, da nicht innerhalb with-Block.
    shp.close()


# Filtern anhand Attribut/anhand Raumbezug

def filter_features_properties(feature, prop):
    """
    Features anhand Attributwerten filtern.
    http://toblerity.org/fiona/manual.html
    To filter features by property values, use Python's builtin filter() and
    lambda or your own filter function that takes a single feature record and
    returns True or False.

    prop = dict {"prop": value}
    """
    return feature['properties'][prop['prop']] == prop['value']


def filter_features_geom(shp, filter_geom):
    """
    Features anhand bounding box bzw. einer Geometrie filtern.

    fiona.Collection.items(): Returns an iterator over FID, record pairs,
    optionally
    filtered by a test for spatial intersection with the provided
    ``bbox``, a (minx, miny, maxx, maxy) tuple or a geometry
    ``mask``.
    A collection’s items() method returns an iterator over pairs of FIDs and records
    that intersect a given (minx, miny, maxx, maxy) bounding box or geometry object.
    The collection’s own coordinate reference system (see below) is used to interpret
    the box’s values.
    If you want a list of the iterator’s items, pass it to Python’s builtin list().

    fiona.Collection.filter(): Returns an iterator over records, but
    filtered by a test for
    spatial intersection with the provided ``bbox``, a (minx, miny,
    maxx, maxy) tuple or a geometry ``mask``.

    filter_geom:
    bbox: {"bbox": (minx, miny, maxx, maxy)}
    mask: {"mask": feature["geometry"]}

    Python built-in filter(function, iterable):

    Construct a list from those elements of iterable for which function returns true.
    Iterable may be either a sequence, a container which supports iteration,
    or an iterator. If iterable is a string or a tuple, the result also has that type;
    otherwise it is always a list. If function is None, the identity function
    is assumed, that is, all elements of iterable that are false are removed.

    """
    with fiona.open(shp) as c:
        if 'bbox' in filter_geom:
            # Iterator ueber IDs und zugehoerigen Features
            feature_items = list(c.items(bbox=filter_geom['bbox']))
            # Iterator ueber Features
            features = list(c.filter(bbox=filter_geom['bbox']))
        elif 'mask' in filter_geom:
            # Iterator ueber IDs und zugehoerigen Features
            feature_items = list(c.items(mask=filter_geom['mask']))
            # Iterator ueber Features
            features = list(c.filter(mask=filter_geom['mask']))

        # Die beiden Iteratoren als Liste in einem Tupel an die aufrufende Funktion zurueckgeben
        return feature_items, features


# Alle Airports in Deutschland in neues Shapefile schreiben:

# Shapefile mit Laender-Geometrien
shp_countries = os.path.join(dir_data,
                             "ne_10m_admin_0_countries.shp")

# Leeres Shapefile mit gleichem Schema wie airports.shp
# Dort hinein sollen alle Airports in Deutschland geschrieben werden.
# Bestehendes Shapefile wird offenbar ohne Warnung von fiona ueberschrieben (im Gegensatz zu GDAL).

#shp_GER = os.path.join(dir_data, "airports_Ire.shp")
#create_shp_from_shp(shp_gdal, shp_GER)

with fiona.open(shp_countries) as c:

    for feature in c:
        #print feature['properties']['NAME']

        # Aus countries ueber Attribut Deutschland finden
        if filter_features_properties(feature, {"prop":"NAME", "value":"Yemen"}):

            # Die Geometrie des Deutschland-Features als Mask fuer raeumlichen Filter nutzen
            features = filter_features_geom(shp_gdal, {"mask":feature["geometry"]})

            # Tupel mit beiden Listen der Iteratoren
            #print features

            #Anzahl Airport-Features in Deutschland: 233

            print len(features[1])
            print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhh'

            # Die Liste an das noch leere Shapefile anhaengen
            # features ist Tupel (items-Iterator, features-Iterator)
            # Features-Iterator in Liste von Features umwandeln und diese in Shapefile schreiben
 #           append_feature(shp_GER, features[1])
