


import os, csv, sqlite3, sys
from distance import calculateTrueDistance
from datetime import datetime

def splitloction( string ):
	
	strings = string.split(",");
	
	numbers = []
	if len( strings ) == 2:
		
		# reverse the order, long and lat wrong way around
		numbers.append( float( strings[1] ) )
		numbers.append( float( strings[0] ) )
		
		#print str( numbers[0] ) + ", " + str( numbers[1] )
		
	return numbers
	
	
def ISOTimeStamp( ts ):
	return datetime.utcfromtimestamp( ts ).isoformat()
	#epoch_start = datetime( 1970, 1, 1, 0, 0 )
	#return epoch_start.utcfromtimestamp(ts).isoformat()

#
#
#
#
	
	
	
print "data2sqlite3.py"

print "Writing database please be patient...."

# distance,changed_method,d,deleted,ts,method_desc,duration,to_loc,device_id,method,from_loc
datafile = sys.argv[1]
databasefile = datafile + '.db'
try:
    os.remove(databasefile)
except OSError:
    pass
	

with open( datafile, 'rb' ) as csvfile:
	reader = csv.DictReader(csvfile)
	header_names = reader.fieldnames
	
	conn = sqlite3.connect(databasefile)
	c = conn.cursor()
	
	c.execute('''CREATE TABLE travel_events (id INTEGER PRIMARY KEY ASC AUTOINCREMENT UNIQUE
				 , changed_method INT
				 , deleted INT
				 , d INT
				 , device_id STRING
				 , ts DATETIME
				 , distance REAL
				 , true_distance REAL
				 , delta_distance REAL
				 , duration REAL
				 , method_desc TEXT
				 , method INT
				 , from_lat REAL
				 , from_long REAL
				 , to_lat REAL
				 , to_long REAL);''')
				 
				 
	for row in reader:	 
		from_loc = splitloction( row['from_loc'] )
		to_loc = splitloction( row['to_loc'] )
		
		#ts =  float( row['ts'] ) /1000
		#iso_ts = ISOTimeStamp( ts )
		
		changed_method = str( row['changed_method'] ) 
		if len(changed_method) == 0:
			changed_method = 'NULL'
		else: 
			changed_method = "'" + changed_method + "'"
		
		true_distance = calculateTrueDistance( from_loc[0], from_loc[1], to_loc[0], to_loc[1] )
		delta_distance  = abs( float( row['distance'] ) - true_distance )
		
		sql_command  = "INSERT INTO travel_events( 'changed_method', 'deleted', 'd', 'device_id', 'ts', 'distance', 'true_distance', 'delta_distance', 'duration', 'method_desc', 'method', 'from_lat', 'from_long', 'to_lat', 'to_long' ) VALUES( " + changed_method + ", NULL, '"+ row['d'] + "', '" + row['device_id'] + "', '" + row['ts'] + "', '" + row['distance'] + "', '" +str(true_distance) + "', '" +str(delta_distance) + "', '"+ row['duration'] + "', '" + row['method_desc'] + "', '" + row['method'] + "', '" + str( from_loc[0] ) + "', '" + str( from_loc[1] ) + "', '" + str( to_loc[0] ) + "', '" + str( to_loc[1] ) + "' )"
			
		c.execute(  sql_command )
		
	conn.commit()
	conn.close()
	
print "database complete. have a nice day :)"

