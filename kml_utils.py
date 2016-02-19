#
#	KML File writing utils
#

# Writes a KML file header
def WriteFileHeader( name, description, xmlfile ):
	xmlfile.write( '<?xml version="1.0" encoding="UTF-8"?>\n' )
	xmlfile.write( '<kml xmlns="http://www.opengis.net/kml/2.2">\n' )
	xmlfile.write( '<Document>\n' )
	xmlfile.write( '<name>'+name+'</name>\n' )
	xmlfile.write( '<description>'+description+'</description>\n' )

# Writes a KML file footer
def WriteFileFooter( xmlfile ): 
	xmlfile.write( '</Document>\n' )
	xmlfile.write( '</kml>\n' )

def WritePinStyle( name, colour, width, xmlfile ):
	xmlfile.write( '<Style id="' + name +'">\n' )
	xmlfile.write( '<IconStyle>\n' )
	xmlfile.write( '<color>' + colour + '</color>\n')
	xmlfile.write( '<scale>' + str(width)+ '</scale>\n' )
	xmlfile.write( '<Icon>\n' )
	xmlfile.write( '<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n' )
	xmlfile.write( '</Icon>\n' )
	xmlfile.write( '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n' )
	xmlfile.write( '</IconStyle>\n' )
	xmlfile.write( '</Style>\n' )

def WriteLineStyle( name, colour, width, xmlfile ):
	xmlfile.write( '<Style id="'+name+'">\n' )
	xmlfile.write( '<LineStyle>\n')
	xmlfile.write( '<color>' + colour + '</color>\n')
	xmlfile.write( '<colorMode>normal</colorMode>\n' )
	xmlfile.write( '<width>' + str(width) + '</width>\n')
	xmlfile.write( '</LineStyle>\n')
	xmlfile.write( '</Style>\n')

def WritePoint( name, latitude, longtitude, style, xmlfile ):
	xmlfile.write( '<Placemark>\n' )
	xmlfile.write( '<styleUrl>#'+ style +'</styleUrl>\n' )
	xmlfile.write( '<name>"' + name + '"</name>\n' )
	xmlfile.write( '<Point>\n' )
	xmlfile.write( '<coordinates>' )
	xmlfile.write( str( longtitude ) + ',' + str( latitude ) + ',0' )
	xmlfile.write( '</coordinates>\n' )
	xmlfile.write( '</Point>\n' )
	xmlfile.write( '</Placemark>\n' )

def WriteLine( name, description, x1, y1, x2, y2, stylename, xmlfile ):
	xmlfile.write( '<Placemark>\n' )
	xmlfile.write( '<name>' + name + '</name>\n' )
	xmlfile.write( '<description>' + description + '</description>' )
	xmlfile.write( '<styleUrl>#' +  stylename + '</styleUrl>\n' )
	xmlfile.write( '<LineString>\n' )
	xmlfile.write( '<gx:altitudeOffset>clampToGround</gx:altitudeOffset>\n' )
	xmlfile.write( '<tessellate>1</tessellate>\n' )
	xmlfile.write( '<coordinates>\n' )
	xmlfile.write( str( x1 ) + ',' + str( y1 ) + ',0\n' )
	xmlfile.write( str( x2 ) + ',' + str( y2 ) + ',0\n' )
	xmlfile.write( '</coordinates>\n' )
	xmlfile.write( '</LineString>\n' )
	xmlfile.write( '</Placemark>\n\n' )

def WriteNetworkLink( name, url, xmlfile ):
	xmlfile.write( '<NetworkLink>\n' )
	xmlfile.write( '<name>' + name + '</name>\n' )
	xmlfile.write( '<Link>\n' )
	xmlfile.write( '<href>' + url + '</href>\n' )
	xmlfile.write( '</Link>\n' )
	xmlfile.write( '</NetworkLink>\n' )

def startFolder( name, isVisible, xmlfile ):
	xmlfile.write('<Folder>\n' )
	xmlfile.write('<name>' + name + '</name>\n' )
	xmlfile.write('<visibility>' + str(isVisible ) + '</visibility>\n' )
	
def endFolder( xmlfile ):
	xmlfile.write('</Folder>\n' )