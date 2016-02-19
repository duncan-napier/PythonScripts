import sys, os, csv 
from datetime import datetime

# split a comma seperated pair of values and swaps their order
def splitAndSwap( string ):
	string = string.replace( '[', '' )
	string = string.replace( ']', '' )
	parts = string.split( ',' )
	new_str = str( parts[1] ) + ", " + str( parts[0] )
	
	return new_str
	
def convertUnixTimeStamp( ts ):
	converted = datetime.fromtimestamp(ts)
	return converted
#	
#
#	Main body of script
#
#


input_path = sys.argv[1]
output_path = os.path.basename( input_path ) + ".polished.csv"

out_file = open( output_path, 'wb' );


print 'reading file ' + input_path
print 'write file ' + output_path


with open( input_path, 'rb' ) as in_file:

	reader = csv.DictReader( in_file )
	writer = csv.DictWriter( out_file, reader.fieldnames )
	
	writer.writeheader()
	
	for row in reader:
		row[ 'from_loc' ] = splitAndSwap( row[ 'from_loc' ] )
		row[ 'to_loc' ]   = splitAndSwap( row[ 'to_loc' ] )
		row[ 'ts' ] = convertUnixTimeStamp( float( int(row['ts'])/1000 ) )
		writer.writerow( row )
		
out_file.close()

