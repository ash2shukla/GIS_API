from flask import Flask, request
from flask_restful import Resource, Api
from CRUD import insertOne,getAllWithinDistance,getWhereIs

app = Flask(__name__)
api = Api(app)

class PostLocation(Resource):
	def post(self):
		'''
		Insert Location corresponding to a pin,address and city
		'''
		request_params = list(request.form.keys())
		expected_params = ['lat','lon','pin','address','city']
		if expected_params == request_params:
			lat = request.form['lat']
			lon = request.form['lon']
			pin = request.form['pin']
			address = request.form['address']
			city = request.form['city']
			code,response = insertOne(lat=lat,lon=lon,pin=pin,address=address,city=city)
			return {'ResponseCode':code,'message':response}
		else:
			for i in expected_params:
				if i not in request_params:
					return {'ResponseCode':'400','message':"Attribute '%s' not in request"%(i)}

class GetUsingPostgres(Resource):
	'''
	Give distance in meters
	'''
	def get(self,lat,lon,distance):
		code,message,pincodes = getAllWithinDistance(lat,lon,distance,'auto')
		return {'ResponseCode':code,'message':message,'data':pincodes}

class GetUsingSelf(Resource):
	'''
	Give distance in meters
	*Uses Haversine for distance computation*

	Takes about 7 seconds to return result
	'''
	def get(self,lat,lon,distance):
		code,message,pincodes = getAllWithinDistance(lat,lon,distance,'manual')
		return {'ResponseCode':code,'message':message,'data':pincodes}

class WhereIs(Resource):
	'''
	Give Lat long in URL
	Returns Place name if exists else returns 'Earth'
	'''
	def get(self,lat,lon):
		code,message,place = getWhereIs(lat,lon)
		return {'ResponseCode':code,'message':message,'data':place}

api.add_resource(PostLocation, '/post_location/')
api.add_resource(GetUsingPostgres, '/get_using_postgres/<float:lat>/<float:lon>/<int:distance>/')
api.add_resource(GetUsingSelf, '/get_using_self/<float:lat>/<float:lon>/<int:distance>/')
api.add_resource(WhereIs, '/where_is/<float:lat>/<float:lon>/')

if __name__ == "__main__":
	app.run(debug=True)
