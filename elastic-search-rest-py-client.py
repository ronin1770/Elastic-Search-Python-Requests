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
		url = config['url'] + "/" + index + "/_doc/_search/?pretty=true" 
		query = {"query" : { "match" : { search_term : return_size }}}
		response = requests.get( url, auth = HTTPBasicAuth(config['username'], config['password']), data=json.dumps(query), headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
		
		if( response.status_code == 200):
			retval = response.text 
		else:
			print( "Connection failed....")
			print( str(response.status_code) + "\n" + response.reason )
		return retval
		
	def search_range(self, index, search_term, lessthan, greaterthan):
		#Searches index for a particular data item for a specified range
		url = config['url'] + "/" + index + "/_doc/_search/?pretty=true" 
		query = {"query" : { "range" : { search_term : { "gte" : greaterthan, "lte" : lessthan } } } }
		# query = {"query" : { "match" : { "pageviews" : "1927" }}}
		response = requests.get( url, auth = HTTPBasicAuth(config['username'], config['password']), data=json.dumps(query), headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
		
		if( response.status_code == 200):
			retval = response.text 
		else:
			print( "Connection failed....")
			print( str(response.status_code) + "\n" + response.reason )
		return retval
		
		
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

	#Create the instance of our client
	esrc =  elastic_search_rest_client()
	
	#Name of our index
	index = "apache_logs"
	
	#Name of the field
	search_term = "pageviews"
	
	#Item we wanted to search
	pageviews    = "1927" 
	
	#Lower bound for search
	lessthan     = "1300" 
	
	#Upper bound for search
	greatherthan = "1200" 
	
	
	"""	
		Uncomment following lines to test
	"""
	
	#Create the index
	#esrc.create_index(index)
	
	# import sample data
	# esrc.import_sample_data(index)
	
	# Get the list of indices
	# esrc.list_indices()
	
	# Get a particular data item (Use an appropriate value of _id. I am using auto-generate IDs - hence they are hexadecimal hash values)
	#print ( esrc.get_data_item(index,_id) )
	
	# Search for pageviews between 1200-1300
	# print( esrc.search_range(index, search_term, lessthan, greaterthan) )
	
	# Search for pageview with given value
	#print( esrc.search_data(index, search_term, 1655) )
	