#
# NaPTAN data to KMLs
#

import datetime, os, sqlite3, sys
from kml_utils import *

# AIR # select * from stops where StopType='AIR' or StopType='GAT'
# RAIL # select * from stops where StopType='RSE' or StopType='RLY' or StopType='RPL'
# FERRY # select * from stops where StopType='FTD' or StopType='FBT' or StopType='FER'
# METRO/TRAM # select * from stops where StopType='TMU' or StopType='MET' or StopType='PLT'
# BUS # select * from stops where StopType='BCE' or StopType='BST' or StopType='BCS' or StopType='BCQ'
# Lift Cable Car # select * from stops where StopType='LCE' or StopType='LPL'
# Taxi # select * from stops where StopType='TXR' or StopType='STR'



def main():
	'''NaPTAN KML file creator'''
	
	start = datetime.datetime.now()
	
	try:
		naptan_db_file = sys.argv[1]
	except IndexError:
		print 'Invalid inputs'
		return
	
	if not os.path.exists( naptan_db_file ):
		print 'Database file ' + naptan_db_file + ' not found'
		return

	modes = [ 'air', 'rail', 'ferry', 'metro', 'bus', 'cable', 'taxi' ]
	select_commands          = {}
	select_commands['air']   = 'select * from stops where StopType=\'AIR\' or StopType=\'GAT\''
	#select_commands['air']   = 'select * from stops where StopType=\'AIR\''
	select_commands['rail']  = 'select * from stops where StopType=\'RSE\' or StopType=\'RLY\' or StopType=\'RPL\''
	select_commands['ferry'] = 'select * from stops where StopType=\'FTD\' or StopType=\'FBT\' or StopType=\'FER\''
	select_commands['metro'] = 'select * from stops where StopType=\'TMU\' or StopType=\'MET\' or StopType=\'PLT\''
	select_commands['bus']   = 'select * from stops where StopType=\'BCE\' or StopType=\'BST\' or StopType=\'BCS\' or StopType=\'BCQ\' or StopType=\'BCT\''
	select_commands['cable'] = 'select * from stops where StopType=\'LCE\' or StopType=\'LPL\''
	select_commands['taxi']  = 'select * from stops where StopType=\'TXR\' or StopType=\'STR\''
	
	mode_desc = {}
	mode_desc['air']   = ( 'Airports'   , 'List of UK Airport locations' )
	mode_desc['rail']  = ( 'Railways'   , 'List of UK Railway locations' )
	mode_desc['ferry'] = ( 'Ferries'    , 'List of UK Ports and Docks locations' )
	mode_desc['metro'] = ( 'Metro/Tram' , 'List of UK Merto/Tram stops' )
	mode_desc['bus']   = ( 'Buses'      , 'List of UK Bus stops and stations' )
	mode_desc['cable'] = ( 'Cable Cars' , 'List of UK Cable Cars` locations' )
	mode_desc['taxi']  = ( 'Taxis'      , 'List of UK Taxi ranks' )
	
	mode_colours = {}
	mode_colours['air']   = 'FF00FFFF'
	mode_colours['rail']  = 'FFFF00FF'
	mode_colours['ferry'] = 'FF00FF00'
	mode_colours['metro'] = 'FFFF00FF'
	mode_colours['bus']   = 'FFFF0000'
	mode_colours['cable'] = 'FF000000'
	mode_colours['taxi']  = 'FF0000FF'
	
	conn = sqlite3.connect(naptan_db_file)
	conn.text_factory = str
	c = conn.cursor()
	
	for mode in modes:
		print 'Creating ' + mode + '.kml'
		
		output_path = 'NaPTAN_' + mode + '.kml'
		try:
			if os.path.exists( output_path ):
				os.remove( output_path )
		except OsError:
			print 'Could not remove ' + output_path
			return
		
		xmlfile = open( output_path, 'w' )
		if xmlfile.closed:
			raise RunTimeError( 'Could not open file for output' )
			
			
		WriteFileHeader( mode_desc[mode][0], mode_desc[mode][1], xmlfile )
		WritePinStyle( mode, mode_colours[mode], 1, xmlfile )
		
		print "Running: " + select_commands[mode]
		rows = c.execute( select_commands[mode] )
		for row in rows:
			try:
			
				name = str( row[4] ).replace( '&', '&amp;' )
				name = name.replace( '<', '&lt;' )
				name = name.replace( '>', '&gt;' )
				WritePoint( name, float( row[30] ), float( row[29] ), mode, xmlfile )
			except:
				print 'it went wrong : ' + str( sys.exc_info()[1] )

		WriteFileFooter( xmlfile )
		xmlfile.close()
		
	delta = datetime.datetime.now() - start
	print 'kml files created in ' + str( delta )
	
	
if __name__ == '__main__':
	main()