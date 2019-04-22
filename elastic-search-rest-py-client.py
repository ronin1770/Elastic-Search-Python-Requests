import requests
import csv
import json
from requests.auth import HTTPBasicAuth
from settings import *


class elastic_search_rest_client:
	def __init__(self):
		#test connection
		response = requests.get( config['url'], auth = HTTPBasicAuth(config['username'], config['password']))
		if( response.status_code == 200):
			print( "Connection successful" )
		else:
			print( "Connection failed....")
			print( str(response.status_code) + "\n" + response.reason )
	
	def create_doc(self, document_name ):
		#Creates the document on the Elasic Search
		print("");
		
	def create_index(self, index):
		#Create the index for the particular document
		url = config['url'] + "/" + index + "?pretty"
		response = requests.put( url, auth = HTTPBasicAuth(config['username'], config['password']))
		if( response.status_code == 200):
			print( response.text )
		else:
			print( "Connection failed....")
			print( str(response.status_code) + "\n" + response.reason )
		
	def list_indices(self):
		#Lists all of the indices on the elastic search cluster
		retval = ""
		
		url = config['url'] + "/_cat/indices"
		response = requests.get( url, auth = HTTPBasicAuth(config['username'], config['password']))
		if( response.status_code == 200):
			retval = response.text
		else:
			print( "Connection failed....")
			print( str(response.status_code) + "\n" + response.reason )
		return retval
		
	def push_data(self, index, json_string):
		#pushes data for the given index
		retval = ""
		
		url = config['url'] + "/" + index + "/_doc" 
		response = requests.post(url, auth = HTTPBasicAuth(config['username'], config['password']), json = json_string )
		
		if( response.status_code == 200 or response.status_code == 201 ):
			retval = response.text
		else:
			print( "Connection failed....")
			print( str(response.status_code) + "\n" + response.reason )
		return retval
		
	def get_data_item(self,index, id):
		retval = ""
		
		url = config['url'] + "/" + index + "/_doc/" + id
		response = requests.get( url, auth = HTTPBasicAuth(config['username'], config['password']))
		if( response.status_code == 200):
			retval = response.text
		else:
			print( "Connection failed....")
			print( str(response.status_code) + "\n" + response.reason )
		return retval
		
	def search_data(self, index, search_term, return_size):
		#retrieves data for the particular search term
		print("");
		
	def search_range(self, index, search_term, lessthan, greaterthan):
		#Searches index for a particular data item for a specified range
		url = config['url'] + "/" + index + "/_doc/_search/?pretty=true" 
		# query = {"query" : { "range" : { "pageviews" : { "gte" : "1200", "lte" : "1250" } } } }
		query = {"query" : { "match" : { "pageviews" : "1927" }}}
		response = requests.get( url, auth = HTTPBasicAuth(config['username'], config['password']), data=json.dumps(query))
		
		if( response.status_code == 200):
			print( response.text )
		else:
			print( "Connection failed....")
			print( str(response.status_code) + "\n" + response.reason )
		# return retval
		
		
	def import_sample_data(self, index):
		#Data is stored in the attached sample.csv
		with open('sample.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					line_count += 1
				else:
					page 		= row[0]
					pageviews 	= row[1]
					unique 		= row[2]
					averagetime = row[3]
					bouncerate  = row[4]

					jsonstring = { "page" : page, "pageviews" : pageviews, "unique" : unique, "averagetime" : averagetime, "bouncerate" : bouncerate }
					self.push_data(index, jsonstring) 
					line_count += 1
					
					print ("Added line #: " + str(line_count))
					
		
if __name__ == "__main__":
	esrc =  elastic_search_rest_client()
	index = "apache_logs"
	search_term = "pageviews"
	
	#json_string = { "ip_address" : "127.0.0.1", "server" : "yayvo", "agent" : "Firefox" }
	#esrc.push_data(index, json_string)
	
	#print ( esrc.get_data_item(index,"kREpRGoBbLLKDSaFGpiw") )
	
	# esrc.import_sample_data(index)
	# print("Data imported")
	esrc.search_range(index, search_term, 1300, 1200)
	