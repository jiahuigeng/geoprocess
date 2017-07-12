import os
from osgeo import ogr

daShapefile = "ne_10m_admin_0_countries.shp"

driver = ogr.GetDriverByName('ESRI Shapefile')

dataSource = driver.Open(daShapefile, 0) # 0 means read-only. 1 means writeable.

# Check to see if shapefile is found.
if dataSource is None:
    print 'Could not open %s' % (daShapefile)
else:
    print 'Opened %s' % (daShapefile)
    layer = dataSource.GetLayer()
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
        print name, pop_est, area#, geom
    layer.ResetReading()
    layer.SetAttributeFilter("") # Attributfilter zuruecksetzen. Bleibt ansonsten fuer "layer" bestehen.
