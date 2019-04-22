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

search_data  => This method will search elastic search cluster for a given term
