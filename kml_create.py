
import sqlite3, sys

from kml_utils import *


if __name__ == '__main__':
	
	db_file = sys.argv[1]
	devices = [] 
	
	conn = sqlite3.connect(db_file)
	c = conn.cursor()
	
	for row in c.execute( "SELECT DISTINCT device_id FROM travel_events ORDER BY device_id ASC" ):
		devices.append( row[0] )
	
	for device in devices:
		sql_command = "SELECT id, ts, method_desc, from_lat, from_long, to_lat, to_long FROM travel_events WHERE device_id ='" + device + "' AND ( ((from_lat >= 50 AND from_lat <= 60 ) AND (from_long >= -11 AND from_long <= 3 ) ) OR ((to_lat >= 50 AND to_lat <= 60 ) AND (to_long >= -11 AND to_long <= 3 ) ) )"
		
		c.execute( sql_command )
		rows = c.fetchall()
		
		if len( rows ) > 0:
			# open file
			filename = device + '_uk.kml'
			xmlfile = open( filename, 'w' )
			if xmlfile.closed:
				raise RunTimeError( 'Could not open file for output' )
			
			WriteFileHeader( 'device + ' + paths, 'Travel events for ' + device, xmlfilr )
			
			WriteLineStyle( 'UnknownPath',     'FF000000', 4, xmlfile )
			WriteLineStyle( 'CarPath',         'FF0000FF', 4, xmlfile )
			WriteLineStyle( 'BikePath',        'FF00FF00', 4, xmlfile )
			WriteLineStyle( 'BusPath',         'FFFF0000', 4, xmlfile )
			WriteLineStyle( 'TrainPath',       'FFFF00FF', 4, xmlfile )
			WriteLineStyle( 'WalkPath',        'FFFFFF00', 4, xmlfile )
			WriteLineStyle( 'AirplanePath',    'FF00FFFF', 4, xmlfile )
			WriteLineStyle( 'NoTransportPath', 'FFFFFFFF', 4, xmlfile )
			
			WritePinStyle( 'StartFrom', 'FF00FF00', 1.3, xmlfile )
			WritePinStyle( 'EndAt',     'FF0000FF', 1.3, xmlfile )
			
			
			stylename = 'UnknownPath'
			for row in rows:
				if row[2] == 'Car' or row[2] == 'CarPetrolSmall':
					stylename = 'CarPath'
				elif row[2] == 'Bicycle': 
					stylename = 'BikePath'
				elif row[2] == 'Bus':
					stylename = 'BusPath'
				elif row[2] == 'InternationalRail' or row[2] == 'Metro' or row[2] == 'NationalRail':
					stylename = 'TrainPath'
				elif row[2] == 'ShortWalk' or row[2] == 'Walk':
					stylename = 'WalkPath'
				elif row[2] == 'Aeroplane':
					stylename = 'AirplanePath'
				elif row[2] == 'Stationary' or row[2] == 'TrainChange':
					stylename = 'NoTransportPath'
				
				xmlfile.write( '<Placemark>\n' )
				xmlfile.write( '<name>' + str( row[0] ) +  '_' + row[2] + '</name>\n' )
				xmlfile.write( '<description> id:' + str( row[0] ) + '<br>TS: ' + row[1] + '<br> Journey Type: ' + row[2] + '<br></description>' )
				xmlfile.write( '<styleUrl>#' +  stylename + '</styleUrl>\n' )
				xmlfile.write( '<LineString>\n' )
				xmlfile.write( '<gx:altitudeOffset>clampToGround</gx:altitudeOffset>\n' )
				xmlfile.write( '<tessellate>1</tessellate>\n' )
				
				xmlfile.write( '<coordinates>\n' )
				
				xmlfile.write( str( row[4] ) + ',' + str( row[3] ) + ',0\n' )
				xmlfile.write( str( row[6] ) + ',' + str( row[5] ) + ',0\n' )
				
				xmlfile.write( '</coordinates>\n' )
				xmlfile.write( '</LineString>\n' )
				xmlfile.write( '</Placemark>\n\n' )
				
				#xmlfile.write( '<Placemark>\n' )
				#xmlfile.write( '<styleUrl>#StartFrom</styleUrl>\n' )
				#xmlfile.write( '<Point>\n' )
				#xmlfile.write( '<coordinates>\n' )
				#xmlfile.write( str( row[4] ) + ',' + str( row[3] ) + ',0\n' )
				#xmlfile.write( '</coordinates>\n' )
				#xmlfile.write( '</Point>\n' )
				#xmlfile.write( '</Placemark>\n\n' )
				
				#xmlfile.write( '<Placemark>\n' )
				#xmlfile.write( '<styleUrl>#EndAt</styleUrl>\n' )
				#xmlfile.write( '<Point>\n' )
				#xmlfile.write( '<coordinates>\n' )
				#xmlfile.write( str( row[6] ) + ',' + str( row[5] ) + ',0\n' )
				#xmlfile.write( '</coordinates>\n' )
				#xmlfile.write( '</Point>\n' )
				#xmlfile.write( '</Placemark>\n' )
				

			WriteFileFooter( xmlfile )
			xmlfile.close()
			