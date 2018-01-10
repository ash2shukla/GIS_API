import unittest
from urllib.request import Request,urlopen
from json import loads
from socket import create_connection
from socket import socket
class TestGETMethods(unittest.TestCase):
	def test_connection(self):
		sock = create_connection(('localhost',5000))
		self.assertIsInstance(sock,socket)
		sock.close()

	def test_pin_using_postgres(self):

		io = [{'ip':'26.1,77.2,50000','op':["202394","202398","476224","476228","476229","476235","485331","485344","814148"]}]
		url = "http://localhost:5000/get_using_postgres/"
		for i in io:
			self.assertEqual(loads(urlopen(Request(url+i['ip'].replace(',','/'))).read())['data'],i['op'])

	def test_pin_using_self(self):
		url = "http://localhost:5000/get_using_self/"
		io = [{'ip':'26.1,77.2,50000','op':["202394","202398","476224","476228","476229","476235","485331","485344","814148"]}]
		for i in io:
			self.assertEqual(loads(urlopen(Request(url+i['ip'].replace(',','/'))).read())['data'],i['op'])

if __name__ == '__main__':
	unittest.main(verbosity=2)
