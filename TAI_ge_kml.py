#
#
# KML file creation
#
#

import os, sqlite3, sys
from kml_utils import *

def singleQuotes( text ):
	return '\'' + text + '\''

def main():
	print 'KML file creation'
	
	db_file = ''
	to_date = ''
	try:
		db_file = sys.argv[1]
		device = sys.argv[2]
		from_date = sys.argv[3]
		to_date = sys.argv[4]
		output = sys.argv[5]
	except IndexError:
		print 'Invalid inputs'
		
	print 'Getting entries for device: ' + device + ' between ' + from_date + ' & ' + to_date
	
	sql_command = 'SELECT id, device_id, ts, distance, duration, method_desc, from_lat, from_long, to_lat, to_long FROM travel_events WHERE device_id=' + singleQuotes(device) + ' AND ts BETWEEN \'' + from_date + '\' AND \'' + to_date + '\''
	print sql_command
	
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		rows = c.execute( sql_command )
		
		xmlfile = open( output, 'w' )
		if xmlfile.closed:
			raise RunTimeError( 'Could not open file for output' )
			return
			
		WriteFileHeader( device, 'Travel events for device ' + device,  xmlfile )
		
		WriteLineStyle( 'UnknownPath',     'FF000000', 4, xmlfile )
		WriteLineStyle( 'CarPath',         'FF0000FF', 4, xmlfile )
		WriteLineStyle( 'BikePath',        'FF00FF00', 4, xmlfile )
		WriteLineStyle( 'BusPath',         'FFFF0000', 4, xmlfile )
		WriteLineStyle( 'TrainPath',       'FFFF00FF', 4, xmlfile )
		WriteLineStyle( 'WalkPath',        'FFFFFF00', 4, xmlfile )
		WriteLineStyle( 'AirplanePath',    'FF00FFFF', 4, xmlfile )
		WriteLineStyle( 'NoTransportPath', 'FFFFFFFF', 4, xmlfile )
		
		stylename = 'UnknownPath'
		for row in rows:
			if row[5] == 'Car' or row[5] == 'CarPetrolSmall':
				stylename = 'CarPath'
			elif row[5] == 'Bicycle': 
				stylename = 'BikePath'
			elif row[5] == 'Bus':
				stylename = 'BusPath'
			elif row[5] == 'InternationalRail' or row[5] == 'Metro' or row[5] == 'NationalRail':
				stylename = 'TrainPath'
			elif row[5] == 'ShortWalk' or row[5] == 'Walk':
				stylename = 'WalkPath'
			elif row[5] == 'Aeroplane':
				stylename = 'AirplanePath'
			elif row[5] == 'Stationary' or row[5] == 'TrainChange':
				stylename = 'NoTransportPath'
		
			WriteLine( str(row[0]), row[5], float( row[6] ), float( row[7] ), float( row[8] ), float( row[9] ), stylename, xmlfile )
			
		WriteFileFooter( xmlfile )
		xmlfile.close()
		
	except:
		print 'Something went horribly wrong... ' + str( sys.exc_info() )
		return
		
	

if __name__ == '__main__':
	main()