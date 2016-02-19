#
#
#	Create NaPTAN sqlite db from cvs files
#
#

import csv, datetime, os, sqlite3, sys

#
#	Function to quote text
#
def quote( string, quote_char = '\"' ):
	return quote_char + string + quote_char

#
# Data types
#
class HeaderTypes:
	STRING = 0
	DATETIME = 1
	INTEGER = 2
	REAL = 3

#
#	column type to sql type
#
def type_2_SQL_type( type ):
	if type == HeaderTypes.STRING:
		return 'STRING'
	elif type == HeaderTypes.DATETIME:
		return 'DATETIME'
	elif type == HeaderTypes.INTEGER:
		return 'INT'
	elif type == HeaderTypes.REAL:
		return 'INT'
	return ''

#
#	column title to type
#
def stop_header_type( name ):
	types = {}
	types['Easting'] = HeaderTypes.REAL
	types['Northing'] = HeaderTypes.REAL
	types['Longitude'] = HeaderTypes.REAL
	types['Latitude'] = HeaderTypes.REAL
	types['CreationDateTime'] = HeaderTypes.DATETIME
	types['ModificationDateTime'] = HeaderTypes.DATETIME
	
	try:
		return types[name]
	except KeyError:
		pass
	return HeaderTypes.STRING

#
#	App entry point,  reads the stops.csv and creates the NaPTAN database
#
def main():
	'''NaPTAN Database creator'''
	
	start = datetime.datetime.now()
	
	try:
		path = sys.argv[1]
	except IndexError:
		print 'Invalid inputs'
		return
	
	stops_file     = path + '/Stops.csv'
	
	# Should include this data as extra tables.
	#air_ref_file   = path + '/AirReferences.csv'
	#alt_desc_file  = path + '/AlternativeDescriptors.csv'
	#coach_ref_file = path + '/CoachReferences.csv'
	#ferry_ref_file = path + '/FerryReferences.csv'
	#rail_ref_file  = path + '/RailReferences.csv'
	
	try:
		naptan_db_file = 'NaPTAN.db'
		if os.path.exists( naptan_db_file ):
			print 'Database Exists, removing file'
			os.remove(naptan_db_file )
	except:
		print 'Could not remove existing database. Is this file opened in another application?'
		return
	
	# Open the csv file
	print 'Writing database...'
	with open( stops_file, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		header_names = reader.fieldnames
		
		# Create table
		sqlcreatetable = 'CREATE TABLE stops ('
		for name in header_names:
			if name == 'AtcoCode':
				header_def = name + ' ' + type_2_SQL_type( stop_header_type( name ) )
			else:
				header_def = ', ' + name +  ' ' + type_2_SQL_type( stop_header_type( name ) )
			sqlcreatetable += header_def
		sqlcreatetable += ' );'
		
		
		conn = sqlite3.connect(naptan_db_file)
		conn.text_factory = str
		
		c = conn.cursor()
		c.execute( sqlcreatetable )
		
		
		# insert data
		for row in reader:
			sqlinsert = 'INSERT INTO stops ('
			for name in header_names:
				if header_names.index( name ) == 0:
					sqlinsert += ' '
				else:
					sqlinsert += ', '
				sqlinsert += quote( name )
			sqlinsert += ' ) VALUES( '
			for name in header_names:
				if header_names.index( name ) == 0:
					sqlinsert += ' '
				else:
					sqlinsert += ', '
					
				dataType = stop_header_type( name )
				if dataType == HeaderTypes.STRING or dataType == HeaderTypes.DATETIME:
					row[name] = row[name].replace( "\"", "'" ) 
					sqlinsert += quote( row[name] )
				else:
					sqlinsert +=row[name]
					
			sqlinsert += ' );'
		
			
			try:
				c.execute( sqlinsert )
			except:
				print 'Error with AtcoCode: ' + row['AtcoCode'] + ' : ' + str( sys.exc_info() )
				print 'CMD: ' + sqlinsert
				
			
	conn.commit()
	conn.close()
	
	delta = datetime.datetime.now() - start
	print 'Database created in ' + str( delta )

if __name__ == '__main__':
	main()