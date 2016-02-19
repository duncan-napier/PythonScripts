

import sqlite3, sys, os, csv 


input_path = sys.argv[1]
output_path = os.path.basename( input_path ) + ".sqlite3"


#conn = sqlite3.connect(output_path)
#c = conn.cursor()

# Create table
#c.execute('''CREATE TABLE journeys IF NOT EXISTS
#             (id int PRIMARY KEY(id, ASC), distance real, change_method text,
#             d int, deleted int, ts int method_description text, duration int''')

with open( input_path, 'rb' ) as in_file:
	reader = csv.DictReader( in_file )
	
	for col in reader:
		print str( col )