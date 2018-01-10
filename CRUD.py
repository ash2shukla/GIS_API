from models import PinMap, FeatureFence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2.functions import ST_AsText, ST_Distance_Sphere, ST_Contains
from urllib.request import urlopen, Request
from csv import reader
from Haversine import haversine
from sys import stdout
from json import loads

db_string = loads(open('config.json').read())['db_uri']
db = create_engine(db_string)

def insertOne(lat,lon,pin,address,city,close_distance=10):
	# close_distance is the value of distance in which if a point exists it will be considered the same
	Session = sessionmaker(db)
	session = Session()
	try:
		float(lat)
		float(lon)

		point = 'POINT(%s %s)'%(lon,lat)
	except Exception as e:
		print('CRUD.insertOne')
		print(type(e))
		return "400","Bad format: Lat/Lon"

	try:
		int(pin)
		if len(pin) != 6:
			return "400","Bad format: pin"
		else:
			key = "IN/"+pin
	except Exception as e:
		print('CRUD.insertOne')
		print(type(e))
		return "400","Bad format: pin"

	# is accuracy = no. of decimal places matching in both of the lat lon ?
	accuracy = abs(len(lon.split('.')[1]) - len(lat.split('.')[1]))

	# Condition - 1  (If Pin Already Exists )
	if session.query(PinMap).filter(PinMap.key == key).count() !=0:
		return "400","Pin already exists"

	# Condition - 2 (If points are close enough)
	if session.query(PinMap).filter(ST_Distance_Sphere(PinMap.location,point) < close_distance ).count() !=0:
		return "400","Point already listed"

	try:
		session.add(PinMap(key=key, place_name=address, admin_name1=city,location=point, accuracy=accuracy))
		session.commit()
		return "200","Success"
	except Exception as e:
		print('CRUD.insertOne')
		print(type(e))
		return "500","Internal Server Error"

def getWhereIs(lat,lon):
	point = 'POINT(%f %f)'%(lon,lat)
	Session = sessionmaker(db)
	session = Session()
	try:
		response = session.query(FeatureFence).filter(ST_Contains(FeatureFence.fence, point))
		if response.count() == 0:
			return "200","Success","Earth ;)"
		else:
			response = response.first()
			return "200","Success",{'city':response.featureName,'state':response.featureParent}
	except Exception as e:
		print('CRUD.getWhereIs')
		print(type(e))
		return "500","Internal Server Error",""

def getAllWithinDistance(lat,lon,distance,method='auto'):
	Session = sessionmaker(db)
	session = Session()
	retval = []
	if method=='auto':
		point = 'POINT(%f %f)'%(lon, lat)
		try:
			for i in session.query(PinMap).filter(ST_Distance_Sphere(PinMap.location,point) < distance):
				retval.append(i.key[3:])
			return "200","Success",retval
		except Exception as e:
			print('CRUD.getAllWithinDistance')
			print(type(e))
			return "500","Internal Server Error",[]
	elif method == 'manual':
		# haversine function defined in Haversine.py
		# Imports all indexed objects and calculates the distance
		# A hybdrid_property or hybrid_function can be implemented as a part of the model to speed up this process
		try:
			# Haversine method is defined in Haversine.py
			for i in session.query(PinMap).all():
				calculated_distance = haversine(session.scalar(i.location.ST_Y()),session.scalar(i.location.ST_X()),lat,lon)
				if calculated_distance < distance:
					print(i.key[3:])
					retval.append(i.key[3:])
			return "200","Success",retval
		except Exception as e:
			print('CRUD.getAllWithinDistance')
			print(type(e))
			return "500","Internal Server Error",[]

def createPinMap(args):
	# WKB POINT stores the data as lon lat instead of lat lon
	try:
		acc = int(args[5])
	except Exception as e:
		#print('CRUD.createPinMap')
		#print(type(e))
		acc = 0
	# Skip rows without lat long
	try:
		# If lat long are not there then skip it
		float(args[3])
		float(args[4])
	except Exception as e:
		#print('CRUD.createPinMap')
		#print(type(e))
		return None

	return PinMap(key=args[0], place_name=args[1], admin_name1=args[2], location='POINT(%s %s)'%(args[4],args[3]), accuracy=acc)

def populateDB():
	Session = sessionmaker(db)
	session = Session()
	csv_url = loads(open('config.json').read())['csv_uri']
	csv_data = urlopen(Request(csv_url)).read().decode('utf-8').split('\n')
	csv_reader = reader(csv_data,delimiter=',',quotechar='|')
	lens = []
	total = 11042
	current = 0
	# skip header
	csv_reader.__next__()
	for i in csv_reader:
		stdout.write('\r')
		stdout.write('percentage complete = %f %%'%((current/total)*100))
		stdout.flush()
		current+=1
		if (len(i) == 6) and (createPinMap(i) is not None):
				session.add(createPinMap(i))
	session.commit()

if __name__ == "__main__":
	populateDB()
