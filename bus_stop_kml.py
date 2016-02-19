
import csv, os, sys

from kml_utils import *



def main():
	csv_file = sys.argv[1]
	print 'Creating kml file for bus stops from ' + csv_file
	output_path = os.path.basename( csv_file ) + '.kml'
	
	xmlfile = open( output_path, 'w' )
	if xmlfile.closed:
		raise RunTimeError( 'Could not open file for output' )
	
	WriteFileHeader( 'UK Bus Stops', 'List of the UK Bus Stops', xmlfile )
	WritePinStyle( 'BusStop', 'FF00FF00', 1, xmlfile )

	count = 0
	with open( csv_file, 'rb' ) as in_file:
		reader = csv.DictReader( in_file )
		for row in reader:
			location = row['Town']
			if len( location ) == 0:
				location = row['LocalityName']
				if len( location ) == 0:
					location = row['ParentLocalityName']
					if len( location ) == 0:
						location = row['GrandParentLocalityName']
				
				try:
					andIx = location.index( '&' )
					location = location.replace( '&', 'and' )
				except ValueError:
					pass
				
			count += 1
			WritePoint( row['Street'] + ', ' + location, row['Latitude'], row['Longitude'], 'BusStop', xmlfile )
			
			if count > 28000:
				break

	WriteFileFooter( xmlfile )
	xmlfile.close()
	
if __name__=='__main__':
	main()