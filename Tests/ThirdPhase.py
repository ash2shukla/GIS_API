import unittest
from urllib.request import Request,urlopen
from json import loads
from socket import create_connection,socket

class TestGETCityMethods(unittest.TestCase):
	def test_connection(self):
		self.assertIsInstance(create_connection(('localhost',5000)),socket)

	def test_res_codes(self):
		io = [{'ip':'10.10,20.20','op':'200'}]
		url = "http://localhost:5000/where_is/"
		for i in io:
			self.assertEqual(loads(urlopen(Request(url+i['ip'].replace(',','/'))).read())['ResponseCode'],i['op'])

	def test_city(self):
		io = [{'ip':"28.450728,76.954750",'op':{'city':'Gurgaon','state':'Haryana'}},\
					{'ip':'28.442923,77.320435','op':{'city':'Faridabad','state':'Haryana'}},\
					{'ip':'28.689944,77.410808','op':{'city':'Ghaziabad','state':'Uttar Pradesh'}},\
					{'ip':'28.513665,77.387131','op':{'city':'Noida','state':'Uttar Pradesh'}},\
					{'ip':'28.542934,77.504996','op':{'city':'Greater Noida','state':'Uttar Pradesh'}},\
					{'ip':'28.490823,77.201941','op':{'city':'South Delhi','state':'Delhi'}},\
					{'ip':'28.566023,76.929527','op':{'city':'South West Delhi','state':'Delhi'}},\
					{'ip':'19.150810,72.835812','op':{'city':'Mumbai','state':'Maharashtra'}}]
		url = "http://localhost:5000/where_is/"

		for i in io:
			self.assertEqual(loads(urlopen(Request(url+i['ip'].replace(',','/'))).read())['data'],i['op'])


if __name__ == '__main__':
	unittest.main(verbosity=2)
