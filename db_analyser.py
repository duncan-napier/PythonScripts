
import os, csv, sqlite3
import sys
import shutil
import math

import matplotlib.lines as lines
import matplotlib.pyplot as plt
import numpy as np

#
#	singleQuotes
#
def singleQuotes( string ):
	quoted = "'" + string + "'"
	return quoted

#	  Aeroplane, Bicycle, Bus, Car, CarPetrolSmall, InternationalRail, Metro, NationalRail, ShortWalk, Stationary, TrainChange, Unknown, Walk
	
#
#	lineColour
#
def lineColour( method_desc ):
	if method_desc == 'Car' or method_desc == 'CarPetrolSmall':
		return 'r'
	elif method_desc == 'Bicycle': 
		return 'g'
	elif method_desc == 'Bus':
		return 'b'
	elif method_desc == 'InternationalRail' or method_desc == 'Metro' or method_desc == 'NationalRail':
		return 'm'
	elif method_desc == 'ShortWalk' or method_desc == 'Walk':
		return 'c'
	elif method_desc == 'Aeroplane':
		return 'y'
	elif method_desc == 'Unknown' or method_desc == 'Stationary' or method_desc == 'TrainChange':
		return 'k'
	else:
		print "Unknown Method description.... " + method_desc
		return 'k'

#
#	arrowedLine
#
def arrowedLine( x0, y0, x1, y1, color, f=0.50 ):
	lines = plt.plot([x0,x1],[y0,y1],color=color, linewidth=2)
	
	f = max(f,.0001)
	dx = f * (x1-x0)
	dy = f * (y1-y0)
	
	a = plt.arrow( x0, y0, dx, dy, color=color, head_width=0.05, head_length=0.1, linewidth=1)
	return lines[0]
	
# ------------------------------------------------------------------------------- #
# entry point of script
# ------------------------------------------------------------------------------- #	
	
databasefile = sys.argv[1]

conn = sqlite3.connect(databasefile)
c = conn.cursor()

c.execute( "SELECT count( id ) FROM travel_events" )
row = c.fetchone()

total_events = int( row[0] )

devices = []
for row in c.execute( "SELECT DISTINCT device_id FROM travel_events" ):
	devices.append( row[0] )
	
methods = []
for row in c.execute( "SELECT DISTINCT method_desc FROM travel_events" ):
	methods.append( row[0] )
	
devices_with_invalid_dates = []
for row in c.execute( "SELECT distinct device_id FROM travel_events WHERE ts > '2016-02-01 00:00:00'" ):
	devices_with_invalid_dates.append( row[0])
	
devices_with_invalid_duration = []
for row in c.execute( "SELECT distinct device_id FROM travel_events WHERE duration < 0" ):
	devices_with_invalid_duration.append( row[0])
	
c.execute( "SELECT count(device_id) FROM travel_events WHERE ts > '2016-02-01 00:00:00'")
invalid_date_count = c.fetchone()[0]

c.execute( "SELECT count(device_id) FROM travel_events WHERE duration < 0")
invalid_duration_count = c.fetchone()[0]

c.execute( "SELECT count(device_id) FROM travel_events WHERE duration == 0")
zero_duration_count = c.fetchone()[0]


c.execute( "SELECT min(ts) FROM travel_events")
earlist_date = c.fetchone()[0]

c.execute( "SELECT max(ts) FROM travel_events")
latest_date = c.fetchone()[0]


print str( total_events ) + " events found."
print str( len( devices ) ) + " devices exists."
print str( len( methods ) ) + " travel methods found."
print "  " + ", ".join( methods )
print ", ".join( devices_with_invalid_dates ) + " devices have invalid dates."
print str( invalid_date_count ) + " entries with invalid date."
print ", ".join( devices_with_invalid_duration ) + " devices have invalid durations."
print str( invalid_duration_count ) + " entries with invalid duration."
print str( zero_duration_count ) + " entries with 0 duration."	
print "Date Range " + earlist_date + " to " + latest_date

device_events = {}



for id in devices:
	sql_commamnd = "SELECT id, device_id, ts, distance, duration, method_desc, from_lat, from_long, to_lat, to_long FROM travel_events WHERE device_id=" + singleQuotes(id)
	c.execute( sql_commamnd )
	rows = c.fetchall();
	device_events[ id ] = rows
	
for device in device_events:
	print device + " : " + str( len( device_events[device] ) ) + " events"
	
plot_folder = 'plots'
try:
	shutil.rmtree(plot_folder)
except OSError:
	pass
os.mkdir( plot_folder )


html_folder = 'html'
try:
	shutil.rmtree(html_folder)
except OSError:
	pass
os.mkdir(html_folder)

# write an html file
html_file = open( 'html/CATCH_data.html', 'w' )
if not html_file.closed:
	
	html_file.write( '<html>' )
	
	html_file.write( '<head>' )
	html_file.write( '<title>' )
	html_file.write( 'CATCH! Data' )
	html_file.write( '</title>' )
	html_file.write( '</head>' )
	
	html_file.write( '<body>' )
	html_file.write( '<center><h1>CATCH Data</h1></center>' )
	
	html_file.write( '<b>' + str( total_events )   + '</b>' + " events found.<br>" )
	html_file.write( '<b>' + str( len( devices ) ) + '</b>' + " devices exists.<br>" )
	html_file.write( '<b>' + str( len( methods ) ) + '</b>' + " travel methods found.<br>" )
	html_file.write( '<ul>' )
	for method in methods:
		html_file.write( '<li><b>' + method + '</b></li>'  )
	html_file.write( '</ul><br>' )

	html_file.write( "Devices have invalid dates.<ul>" )
	for device in devices_with_invalid_dates:
		html_file.write( '<li><b>' + device + '</b></li>'  )
	html_file.write( '</ul><br>' )
	
	html_file.write( "<b>" + str( invalid_date_count ) + "</b> entries with invalid date.<br>" )
	
	html_file.write( "Devices have invalid durations.<ul>" )
	for device in devices_with_invalid_duration:
		html_file.write( '<li><b>' + device + '</b></li>'  )
	html_file.write( '</ul><br>' )
	
	html_file.write( "<b>" + str( invalid_duration_count ) + "</b> entries with invalid duration.<br>" )
	html_file.write( "<b>" + str( zero_duration_count ) + "</b> entries with 0 duration.<br>" )
	html_file.write( "Date Range <b>" + earlist_date + "</b> to <b>" + latest_date+ "</b><br>" )
	
	html_file.write( 'Devices:<br><ul>' )
	for device in device_events:
		html_file.write( '<li><a href="' + device + '.html">' + device + '</a></li>' )
		
	
	html_file.write( '</ul>' )
	html_file.write( '</body>' )
	html_file.write( '</html>' )
	
	html_file.close()
		
	
for device in device_events:
		
	device_events_by_type = {}
	
	for method in methods:
		device_events_by_type[ method ] = []
		
	for row in device_events[device]:
		device_events_by_type[ row[5] ].append( row )
		
		
	# all events
	draw_plots = True
	
	lines = []
	legendMethods = []
	if draw_plots == True:
		plt.title( device )
		plt.xlabel('Latitude')
		plt.ylabel('Longitude')
	
		for row in device_events[device]:
			new_line = arrowedLine( row[6], row[7], row[8], row[9], lineColour(row[5]) )
			
			if row[5] not in legendMethods:
				new_line.set_label( row[5] )
				legendMethods.append( row[5] )
			
		plt.legend()
			
    
		fig = plt.gcf()
		fig.savefig( "plots/" + device + '_journey_plots.png', bbox_inches='tight', dpi=96 )
		plt.close(fig) 
	
		#
		for method_desc in device_events_by_type:
			if len( device_events_by_type[method_desc] ) == 0:
				continue
			plt.title( device + " " + method_desc )
			plt.xlabel('Latitude')
			plt.ylabel('Longitude')
			for row in device_events_by_type[method_desc]:
				new_line = arrowedLine( row[6], row[7], row[8], row[9], lineColour(method_desc) )
	
			fig = plt.gcf()
			fig.savefig( "plots/" + device + '_' + method_desc + '_journey_plots.png', bbox_inches='tight', dpi=96 )
			plt.close(fig) 
		
	
	html_file = open( 'html/'+device+'.html', 'w' )
	if not html_file.closed:
		html_file.write( '<html>' )
	
		html_file.write( '<head>' )
		html_file.write( '<title>' )
		html_file.write( 'CATCH! Data' )
		html_file.write( '</title>' )
		html_file.write( '</head>' )
		
		html_file.write( '<body>' )
		html_file.write( '<center><h1>CATCH Data for Device' + device + '</h1></center>' )
		html_file.write( '<h2><center>All Events<center></h2><hr><br>' )
		html_file.write( '<img src="' + '../plots/' + device + '_journey_plots.png' + '">' )
		for method_desc in device_events_by_type:
			if len( device_events_by_type[method_desc] ) == 0:
				continue
			html_file.write( '<h2><center>' + method_desc + '</center></h2><hr><br>' )
			html_file.write( '<img src="' '../plots/' + device + '_' + method_desc + '_journey_plots.png' + '"><br>' )
		
		html_file.write( '</body>' )
		html_file.write( '</html>' )
		
		html_file.close()