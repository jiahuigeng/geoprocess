# _*_ coding : utf-8 _*_

import os
import csv
from osgeo import ogr, osr, gdal




class Airport(object):
	def __init__(self, name, country, iata, icao, lat, lon,f_out=0, f_in =0 ):
		self.name = name
		self.country = country
		self.iata = iata
		self.icao = icao
		self.f_out = f_out
		self.f_in = f_in
		self.lat =lat
		self.lon =lon


if __name__=='__main__':
	airports=[]
	iata = {}
	icao = {}
	dir_script = os.path.abspath(os.path.dirname(__file__))
	dir_ap = os.path.join(dir_script, "airports.dat")
	dir_aline = os.path.join(dir_script, "routes.dat")
	with open(dir_ap) as csvfile:
		
		fieldnames = ["airport_ID", "name", "city", "country", "iata", "icao",
			          "lat", "lon", "alt", "tz", "dst", "dtz", "type", "src"]

		data = csv.DictReader(csvfile, fieldnames)
		for row in data:
			ap=Airport(row["name"],row["country"],row["iata"],row["icao"],row['lat'],row['lon'])
			airports.append(ap)
			iata[row["iata"]]=row["country"]
			icao[row["icao"]]=row["country"]

	with open(dir_aline) as csvline:
		fieldnames_1=['airline','airline_id','src_ap','src_id','dest_ap','dest_id','x','y','z']
		data_1 = csv.DictReader(csvline, fieldnames_1)
		for row_1 in data_1:
			flag_out= False
			flag_in = False
			if row_1['src_ap'] in iata:
				flag_out=True
			if row_1['dest_ap'] in iata:
				flag_in=True

			if flag_out == True and flag_in == True:
				for ap_t in airports:
					if ap_t.iata==row_1['src_ap']:
						ap_t.f_out=ap_t.f_out+1
					if ap_t.iata==row_1['dest_ap']:
						ap_t.f_in=ap_t.f_in+1
#	for ap_t in airports:					
#		print ap_t.name+" "+ str(ap_t.f_out) + ' ' + str(ap_t.f_in)




	dir_shpap = os.path.join(dir_script, "airports_new.shp")
	driver = ogr.GetDriverByName('ESRI Shapefile')

	if os.path.exists(dir_shpap): #Alternative: os.path.isfile(dir_shpap):
	    driver.DeleteDataSource(dir_shpap)
	shp = driver.CreateDataSource(dir_shpap)

	# Spatial Reference des Shapefiles definieren
	srs = osr.SpatialReference()
	srs.ImportFromEPSG(4326) # EPSG:4326 ist WGS1984

	# Layer anlegen: Soll Punkt-Geometrien enthalten.
	layer = shp.CreateLayer("layer", srs, ogr.wkbPoint)

	# Attributfelder des Layers und deren Datentypen definieren
	field_name = ogr.FieldDefn("name", ogr.OFTString)
	layer.CreateField(field_name)
	field_lat = ogr.FieldDefn("lat", ogr.OFTReal)
	layer.CreateField(field_lat)
	field_lon = ogr.FieldDefn("lon", ogr.OFTReal)
	layer.CreateField(field_lon)
	field_fout = ogr.FieldDefn("flight_out", ogr.OFTInteger) # Feld definieren
	layer.CreateField(field_fout) # Feld erstellen
	field_fin = ogr.FieldDefn("flight_out", ogr.OFTInteger) # Feld definieren
	layer.CreateField(field_fin) # Feld erstellen

	for ap_t in airports:
		#print ap_t.name+" "+ str(ap_t.f_out) + ' ' + str(ap_t.f_in)
    # Feature anlegen und Werte aus csv in shp-Attribute schreiben
	    feature = ogr.Feature(layer.GetLayerDefn())
	    feature.SetField("name", ap_t.name)
	    feature.SetField("lat", ap_t.lat)
        feature.SetField("lon", ap_t.lon)
        feature.SetField("flight out", ap_t.f_out)
        feature.SetField("flight in", ap_t.f_in)

        # Feature-Geometrie als Well-Known-Text aus den lat-/Lon-Strings erzeugen
        wkt = "POINT({0} {1} {2} {3})".format(ap_t.lat, ap_t.lon,ap_t.f_out,ap_t.f_in)
        point = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point)
        layer.CreateFeature(feature)
        del feature
	del shp



