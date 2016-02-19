import csv, os, sys

from kml_utils import *
from bng_convertor import *

def main():
	csv_file = sys.argv[1]
	print 'Creating kml file for bus stops from ' + csv_file
	output_path = os.path.basename( csv_file ) + '.kml'
	
	xmlfile = open( output_path, 'w' )
	if xmlfile.closed:
		raise RunTimeError( 'Could not open file for output' )
	
	WriteFileHeader( 'UK Train Stations', 'List of the UK TrainStations', xmlfile )
	WritePinStyle( 'TrainStation', 'FFFF00FF', 1, xmlfile )
	
	with open( csv_file, 'rb' ) as in_file:
		reader = csv.DictReader( in_file )
		for row in reader:
			easting 	= float( row['Easting']  )
			northing 	= float( row['Northing'] )
			name		= row['StationName']
			lat_long	= BNG2toLatLong( easting, northing )
			
			try:
				andIx = name.index( '&' )
				name  = name.replace( '&', 'and' )
			except ValueError:
				pass
					
			WritePoint( name, lat_long[0], lat_long[1], 'TrainStation', xmlfile )
		
		WriteFileFooter( xmlfile )
		xmlfile.close()
	
if __name__=='__main__':
	main()