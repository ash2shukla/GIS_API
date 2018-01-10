from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from math import sqrt,radians,sin,cos,atan2
from json import loads

db_string = loads(open('config.json').read())['db_uri']

db = create_engine(db_string)

base = declarative_base()

class PinMap(base):
	__tablename__ = 'pinmaps'

	key = Column(String,primary_key=True)
	place_name = Column(String)
	admin_name1 = Column(String)
	location = Column(Geometry('POINT'))
	accuracy = Column(Integer)

class FeatureFence(base):
	__tablename__ = 'featurefences'

	id = Column(Integer, primary_key=True)
	featureName = Column(String)
	featureType = Column(String)
	# If parent is also a feature we may declare it as a foreignKey
	featureParent = Column(String)
	fence = Column(Geometry('POLYGON'))

# Run models.py directly to init tables

if __name__ == "__main__":
	base.metadata.create_all(db)
