#
#
#	Maximum extraction
#
#

import datetime, os, shutil, sqlite3, sys
import dateutil.parser

from kml_utils import *

def singleQuotes( text ):
	return '\'' + text + '\''
	
class event:
	def __init__( self, id, change_method, ts, distance, true_distance, delta_distance, duration, method_desc, from_lat, from_long, to_lat, to_long ):
		self.id = id
		self.change_method = change_method
		self.ts = ts
		self.distance = distance
		self.true_distance = true_distance
		self.delta_distance = delta_distance
		self.duration = duration
		self.method_desc = method_desc
		self.from_lat = from_lat
		self.from_long = from_long
		self.to_lat = to_lat
		self.to_long = to_long

# returns a list of all available device ids.
def get_device_list( cursor ):
	devices = []
	try:
		sql_command = 'SELECT DISTINCT(device_id) FROM travel_events'
		for row in cursor.execute( sql_command ):
			devices.append( row[0] )
	except Exception as e:
		raise e
		
	return devices

# returns the active ranges
def get_device_date_range( device_id, cursor ):
	dates = []
	try:
		sql_command = 'SELECT min(ts), max(ts) FROM travel_events WHERE device_id='+ singleQuotes( device_id )
		cursor.execute( sql_command )
		row = cursor.fetchone()

		dates.append( dateutil.parser.parse( row[0] ) )
		dates.append( dateutil.parser.parse( row[1] ) )
		
	except Exception as e:
		print 'Error in date range'
		raise e
	return dates


#  returns all events for a given device id and date range
def get_all_events( device_id, from_date, to_date, cursor ):
	events = []
	try:
		sql_command = 'SELECT id, changed_method, ts, distance, true_distance, delta_distance, duration, method_desc, method, from_lat, from_long, to_lat, to_long FROM travel_events WHERE device_id =' + singleQuotes( device_id ) + ' AND ts BETWEEN ' + singleQuotes( str( from_date ) ) + ' AND ' + singleQuotes( str( to_date ) )
		
		for row in cursor.execute( sql_command ):
			id = int( row[0] )
			change_method = 0
			if  len( str( row[1] ) ) > 0:
				change_method = str( row[1] )
			ts = dateutil.parser.parse( row[2] )
			dist = float( row[3] )
			true_dist = float( row[4] )
			delta_dist = float( row[5] )
			duration = float( row[6] )
			method_desc = row[7]
			method = int( row[8] )
			from_lat = float( row[9] )
			from_long = float( row[10] )
			to_lat = float( row[11] )
			to_long = float( row[12] )
			events.append( event( id, change_method, ts, dist, true_dist, delta_dist, duration, method_desc, from_lat, from_long, to_lat, to_long ) )
			
	except Exception as e:
		print 'Get Events error...' 
		raise e
	return events

def get_uk_events( device_id, from_date, to_date, cursor ):
	events = []
	try:
		sql_command = 'SELECT id, changed_method, ts, distance, true_distance, delta_distance, duration, method_desc, method, from_lat, from_long, to_lat, to_long FROM travel_events WHERE device_id =' + singleQuotes( device_id ) + ' AND ( ((from_lat >= 50 AND from_lat <= 60 ) AND (from_long >= -11 AND from_long <= 3 ) ) OR ((to_lat >= 50 AND to_lat <= 60 ) AND (to_long >= -11 AND to_long <= 3 ) ) ) AND (ts BETWEEN ' + singleQuotes( str( from_date ) ) + ' AND ' + singleQuotes( str( to_date ) ) + ')'
		
		#print sql_command
		
		for row in cursor.execute( sql_command ):
			id = int( row[0] )
			change_method = 0
			if  len( str( row[1] ) ) > 0:
				change_method = str( row[1] )
			ts = dateutil.parser.parse( row[2] )
			dist = float( row[3] )
			true_dist = float( row[4] )
			delta_dist = float( row[5] )
			duration = float( row[6] )
			method_desc = row[7]
			method = int( row[8] )
			from_lat = float( row[9] )
			from_long = float( row[10] )
			to_lat = float( row[11] )
			to_long = float( row[12] )
			events.append( event( id, change_method, ts, dist, true_dist, delta_dist, duration, method_desc, from_lat, from_long, to_lat, to_long ) )
			
	except Exception as e:
		print 'Get Events error...' 
		raise e
	return events

# creates the style definations for a kml file
def write_line_styles( xmlfile ):
	if xmlfile.closed:
		raise RunTimeError( 'Could not open file for output' )
		
	WriteLineStyle( 'UnknownPath',     'FF000000', 4, xmlfile )
	WriteLineStyle( 'CarPath',         'FF0000FF', 4, xmlfile )
	WriteLineStyle( 'BikePath',        'FF00FF00', 4, xmlfile )
	WriteLineStyle( 'BusPath',         'FFFF0000', 4, xmlfile )
	WriteLineStyle( 'TrainPath',       'FFFF00FF', 4, xmlfile )
	WriteLineStyle( 'WalkPath',        'FFFFFF00', 4, xmlfile )
	WriteLineStyle( 'AirplanePath',    'FF00FFFF', 4, xmlfile )
	WriteLineStyle( 'NoTransportPath', 'FFFFFFFF', 4, xmlfile )
	
def method_style( method_desc ):
	stylename = 'UnknownPath'
	if method_desc == 'Car' or method_desc == 'CarPetrolSmall':
		stylename = 'CarPath'
	elif method_desc == 'Bicycle': 
		stylename = 'BikePath'
	elif method_desc == 'Bus':
		stylename = 'BusPath'
	elif method_desc == 'InternationalRail' or method_desc == 'Metro' or method_desc == 'NationalRail':
		stylename = 'TrainPath'
	elif method_desc == 'ShortWalk' or method_desc == 'Walk':
		stylename = 'WalkPath'
	elif method_desc == 'Aeroplane':
		stylename = 'AirplanePath'
	elif method_desc == 'Stationary' or method_desc == 'TrainChange':
		stylename = 'NoTransportPath'
	return stylename

# creates an kml file of the travel events
def create_events_kml( name, description, events, filepath ):
	xmlfile = open( filepath, 'w' )
	if xmlfile.closed:
		raise RunTimeError( 'Could not open file for output' )
		
	WriteFileHeader( name, description,  xmlfile )
	write_line_styles( xmlfile )
	
	for evt in events:
		style = method_style( evt.method_desc )
		WriteLine( str( evt.id ), evt.method_desc, evt.from_lat, evt.from_long, evt.to_lat, evt.to_long, style, xmlfile )
	
	WriteFileFooter( xmlfile )
	xmlfile.close()


def create_unified_kml( name, description, device_files, device_uk_files, filepath ):
	try:
		xmlfile = open( filepath, 'w' )
		if xmlfile.closed:
			raise RunTimeError( 'Could not open file for output' )
			
		WriteFileHeader( name, description, xmlfile )
		
		startFolder( 'Legend', 1, xmlfile )
		WriteNetworkLink( 'Journey Legend', 'scale.kml', xmlfile )
		endFolder( xmlfile )
		
		startFolder( 'All Events By Day', 0, xmlfile )
		for device in device_files:
			startFolder( device, 0, xmlfile )
			for file in device_files[device]:
				name = ''
				try:
					filename = os.path.split( file )[1]
					name = filename[-12:-4]
				except:
					print 'Error: ' + str( sys.exc_info() )
					
				WriteNetworkLink( name, filename, xmlfile )
				
			endFolder( xmlfile )
		endFolder( xmlfile )
		
		startFolder( 'All UK Events By Day', 0, xmlfile )
		for device in device_uk_files:
			startFolder( 'uk_' + device, 0, xmlfile )
			for file in device_uk_files[device]:
				name = ''
				try:
					filename = os.path.split( file )[1]
					name = filename[-12:-4]
				except:
					print 'Error: ' + str( sys.exc_info() )
				WriteNetworkLink( name, filename, xmlfile )
			endFolder( xmlfile )
		endFolder( xmlfile )
		
		WriteFileFooter( xmlfile )
		xmlfile.close()
	except:
		print 'create_unified_kml error ' + str( sys.exc_info() )
		

# main entry point for the app
def main():

	db_file = ''
	kml_folder = 'travel_ai_kml'
	
	try:
		db_file = sys.argv[1]
		
	except IndexError:
		print 'Invalid input arguments.'
		
	if not os.path.exists( db_file ):
		raise RuntimeError( db_file + ' not found.' )
		
	if os.path.exists(kml_folder):
		shutil.rmtree( kml_folder )
	os.makedirs( kml_folder )
	
	# copy scale.png and scale.kml to kml_folder
	image_file = 'scale.png'
	kml_file = 'scale.kml'
	
	missing_files = False
	if not os.path.exists( image_file ):
		missing_files = True
		print 'Missing: ' + image_file
	if not os.path.exists( kml_file ):
		missing_files = True
		print 'Missing: ' + kml_file
		
	if missing_files:
		raise RuntimeError( 'Missing scale files' )
		
	shutil.copyfile( image_file, os.path.join( kml_folder, image_file ) )
	shutil.copyfile( kml_file, os.path.join( kml_folder, kml_file ) )
	
	print 'Reading from ' + db_file
	
	try:
		# connect to db
		conn = sqlite3.connect(db_file)
		conn.text_factory = str
		c = conn.cursor()
		
		# set up data list
		devices = get_device_list( c )
		device_all_files = {}
		device_uk_files = {}
		
		# for each device
		for device in devices:
			print 'Device: ' + device
			dates = get_device_date_range( device, c )
			cur_date = dates[0] 
			
			# create individual day event list kml files
			while cur_date <= dates[1]:
				date1    = datetime.datetime( cur_date.year, cur_date.month, cur_date.day, 0, 0, 0 )
				date2    = datetime.datetime( cur_date.year, cur_date.month, cur_date.day, 23, 59, 59 )
				events   = get_all_events( device, date1, date2, c )
				filename = os.path.join( kml_folder, device + cur_date.strftime( "_%Y%m%d" ) + '.kml' )
				
				if len( events ) > 0:
					name = device + ' travel events'
					description =  'events for ' + date1.strftime('%d%m%Y')
					create_events_kml( name, description, events, filename )
					
					# store filename of the event list
					if device not in device_all_files:
						device_all_files[device] = []
						
					device_all_files[device].append( filename )
				
				events   = get_uk_events( device, date1, date2, c )
				if len( events ) > 0:
					name = device + ' UK travel events'
					description =  'UK events for ' + date1.strftime('%d%m%Y')
					
					filename = os.path.join( kml_folder, device + cur_date.strftime( "_UK_%Y%m%d" ) + '.kml' )
					create_events_kml( name, description, events, filename )
					
					if device not in device_uk_files:
						device_uk_files[device] = []
					device_uk_files[device].append( filename )
				
				
				cur_date += datetime.timedelta(days=1)
			
		# create unified KML file
		unified_file_name = os.path.join( kml_folder, 'All_Journies.kml' )
		name = 'Travel AI data'
		description = 'All events from the sample data'
		create_unified_kml( name, description, device_all_files, device_uk_files, unified_file_name )
		
	except Exception as e:
		print 'Error: ' + str( sys.exc_info()[0] ) + ' ' + str( sys.exc_info() )
#
if __name__ == '__main__':
	try:
		main()
	except RuntimeError as error:
		print 'Error: ' + str( e.errorno )