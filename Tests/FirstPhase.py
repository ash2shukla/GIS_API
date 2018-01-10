import unittest
from socket import create_connection
from socket import socket
from requests import post
from json import loads

class TestPOSTMethods(unittest.TestCase):
	def test_connection(self):
		sock = create_connection(("localhost",5000))
		self.assertIsInstance(sock,socket)
		sock.close()

	def test_response(self):
		io = [{"ip":{"lat":"xyz","lon":"abc","pin":"111111","address":"test_address","city":"test_city"},"op":{"ResponseCode":"400","message":"Bad format: Lat/Lon"}},\
			{"ip":{"lat":"1.1","lon":"2.2","pin":"xyzabc","address":"test_address","city":"test_city"},"op":{"ResponseCode":"400","message":"Bad format: pin"}},\
			{"ip":{"lat":"1.1","lon":"2.2","pin":"11111","address":"test_address","city":"test_city"},"op":{"ResponseCode":"400","message":"Bad format: pin"}},\
			{"ip":{"lat":"1.1","lon":"2.2","pin":"209801","address":"test_address","city":"test_city"},"op":{"ResponseCode":"400","message":"Pin already exists"}}]
		url = "http://localhost:5000/post_location/"
		for i in io:
			self.assertEqual(loads(post(url,data=i['ip']).text),i["op"])

if __name__ == "__main__":
	unittest.main(verbosity=2)
