from models import FeatureFence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.request import urlopen, Request
from json import loads

# {
# 	'type': 'FeatureCollection',
# 	'features':[
# 		{'type':'Feature','properties':{'name':'featureName' (Here City Name)
# 										'type':'featureType' (Here City)
# 										'parent':'parentFeature?' (Here State Name)
# 										},
# 						'geometry':{
# 						'type':'geometryType' <Polygon>
# 						'coordinates':[ [ [lat,lng]...[lat,lng] ] ] <There might exist more than one polygons foe one feature>
# 						}
# 		} ...]
# }

# Each feature's each polygon will be indexed as an entry in database

def createPolygon(lat_lng_array=[]):
	print('\t|\t|\t|-Coordinates in polygon %d '%len(lat_lng_array))
	start = 'POLYGON(('
	end = '))'
	length = len(lat_lng_array)
	mid = ("%s %s,"*length)[:-1] # remove one extra comma
	args = []
	for i in lat_lng_array:
		args+=[i[0],i[1]]

	args = tuple(args)

	return (start+mid+end)%args


def parseFeature(Feature={'type':'Feature','properties':{'type':''},'geometry':{'type':'','coordinates':[]}}):
	db_string = loads(open('config.json').read())['db_uri']
	db = create_engine(db_string)
	Session = sessionmaker(db)
	session = Session()

	if Feature['type'] == 'Feature':
		# A unique entry will be for each polygon of a feature with same properties
		print("\t|-Polygons in Feature %s = %d"%(Feature['properties']['name'],len(Feature['geometry']['coordinates'])))
		print('\t|\t|-Adding to session')
		for i in Feature['geometry']['coordinates']:
			ff = FeatureFence(featureType = Feature['properties']['type'],\
					featureName = Feature['properties']['name'],\
					featureParent = Feature['properties']['parent'],\
					fence = createPolygon(i))
			session.add(ff)
		print('\t|\t|-Added')
	session.commit()

def parseRoot(geoJson={'type':'','features':[]}):
	if geoJson['type'] == 'FeatureCollection':
		print('Total Number of Features is = %d'%len(geoJson['features']))
		for i in geoJson['features']:
			parseFeature(i)
		print('Done!')

if __name__ == "__main__":
	url = loads(open('config.json').read())['geojson_uri']
	data = urlopen(Request(url)).read().decode('utf-8')
	parseRoot(loads(data))
