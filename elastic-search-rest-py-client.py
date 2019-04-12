import requests
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
		#Creates the document on the Elastic Search
		
	def create_index(self, document_name, index):
		#Create the index for the particular document
		
	def list_indices(self):
		#Lists all of the indices on the elastic search cluster
		
	def push_data(self, index, json_string):
		#pushs data for the given index
		
	def search_data(self, index, search_term, return_size):
		#retrieves data for the particular search term
		
if __name__ == "__main__":
	esrc =  elastic_search_rest_client()