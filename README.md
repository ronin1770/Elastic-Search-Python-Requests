# Elastic-Search-Python-Requests
Simple code that demostrates the working of elastic search using Python 3.5+ and requests package

This is a simple project to illustrate how to access Elastic Search with Python (using requests package). 

Credentials are stored in settings.py

     config = {
			'username' : '',
			'password' : '',
			'url'	 : ''
	}

This project will have following methods:

_init_       => When class is instantiated it will test the connection   
     
create_doc   => This method will create document type in the elastic search

create_index => This method will create an index for a given document type

	def create_index(self, index):
			#Create the index for the particular document
			url = config['url'] + "/" + index + "?pretty"
			response = requests.put( url, auth = HTTPBasicAuth(config['username'], config['password']))
			if( response.status_code == 200):
				print( response.text )
			else:
				print( "Connection failed....")
				print( str(response.status_code) + "\n" + response.reason )

list_indices => This method will list all indices on the cluser
	
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

push_data    => This method will be used for pushing data to the cluser

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

search_data  => This method will search elastic search cluster for a given term

get_data_item 	=> This method retrieves a particular data item using its _id

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

import_sample_data => This method pushes data from the sample file into the Elastic Search

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
