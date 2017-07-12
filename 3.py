import os
import fiona
from osgeo import ogr, osr, gdal

daShapefile = "airports_new.shp"

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
