'''
http://www.hannahfry.co.uk/blog//2011/10/10/converting-british-national-grid-to-latitude-and-longitude
Contains functions for converting to and from BNG ( Bristish National Grid )
'''

import math, sys

def BNG2toLatLong(E,N):

	'''E, N are the British national grid coordinates - eastings and northings'''
	a, b 	= 6377563.396, 6356256.909	# The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
	F0		= 0.9996012717				# scale factor on the central meridian
	lat0 	= 49*math.pi/180 			# Latitude of true origin (radians)
	lon0 	= -2*math.pi/180			# Longtitude of true origin and central meridian (radians)
	N0, E0 	= -100000, 400000			# Northing & easting of true origin (m)
	e2		= 1 - (b*b)/(a*a)			# eccentricity squared
	n = (a-b)/(a+b)
	
	#Initialise the iterative variables
	lat,M = lat0, 0
	
	while N-N0-M >= 0.00001: #Accurate to 0.01mm
		lat = ( N - N0 - M ) / ( a * F0 ) + lat
		M1  = ( 1 + n + (5./4)*n**2 + (5./4)*n**3) * (lat-lat0)
		M2  = ( 3*n + 3 * n ** 2 + ( 21.0 / 8) * n ** 3 ) * math.sin( lat - lat0 ) * math.cos( lat + lat0 )
		M3  = ( (15.0 / 8 ) * n ** 2 + ( 15.0 / 8 ) * n ** 3 ) * math.sin( 2 * ( lat-lat0 ) ) * math.cos( 2 * ( lat + lat0 ) )
		M4  = ( 35.0 / 24 ) * n ** 3 * math.sin( 3 * ( lat - lat0 ) ) * math.cos(3*(lat+lat0))
		#meridional arc
		M = b * F0 * (M1 - M2 + M3 - M4)          
	
	#transverse radius of curvature
	nu = a*F0/math.sqrt(1-e2*math.sin(lat)**2)
	
	#meridional radius of curvature
	rho = a*F0*(1-e2)*(1-e2*math.sin(lat)**2)**(-1.5)
	eta2 = nu/rho-1
	
	secLat = 1.0/math.cos(lat)
	VII    = math.tan(lat) / ( 2 * rho * nu )
	VIII   = math.tan(lat) / ( 24 * rho * nu ** 3 ) * ( 5 + 3 * math.tan(lat) ** 2 + eta2 - 9 * math.tan(lat) ** 2 * eta2 )
	IX     = math.tan(lat) / ( 720 * rho * nu ** 5 ) * ( 61 + 90 * math.tan(lat) ** 2 + 45 * math.tan(lat) ** 4 )
	X      = secLat/nu
	XI     = secLat / ( 6 * nu ** 3 ) * ( nu / rho + 2 * math.tan(lat) ** 2 )
	XII    = secLat / ( 120 * nu ** 5 ) * ( 5 + 28 * math.tan(lat) ** 2 + 24 * math.tan(lat) ** 4 )
	XIIA   = secLat / ( 5040 * nu ** 7 ) * ( 61 + 662 * math.tan(lat) ** 2 + 1320 * math.tan(lat) ** 4 + 720 * math.tan(lat) ** 6 )
	dE     = E-E0
	
	#These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
	lat_1 = lat - VII*dE**2 + VIII*dE**4 - IX*dE**6
	lon_1 = lon0 + X*dE - XI*dE**3 + XII*dE**5 - XIIA*dE**7
	
	#Want to convert to the GRS80 ellipsoid. 
	#First convert to cartesian from spherical polar coordinates
	H = 0 # Third spherical coord. 
	x_1 = (nu/F0 + H) * math.cos(lat_1) * math.cos(lon_1)
	y_1 = (nu/F0 + H) * math.cos(lat_1) * math.sin(lon_1)
	z_1 = ( (1-e2) * nu/F0 + H  )* math.sin(lat_1)
	
	#Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
	s = -20.4894*10**-6 #The scale factor -1
	tx, ty, tz = 446.448, -125.157, + 542.060	# The translations along x,y,z axes respectively
	rxs,rys,rzs = 0.1502,  0.2470,  0.8421		# The rotations along x,y,z respectively, in seconds
	rx, ry, rz = rxs * math.pi/(180*3600.0), rys * math.pi/(180*3600.0), rzs * math.pi/(180*3600.0) #In radians
	x_2 = tx + (1+s)*x_1 + (-rz)*y_1 + (ry)*z_1
	y_2 = ty + (rz)*x_1  + (1+s)*y_1 + (-rx)*z_1
	z_2 = tz + (-ry)*x_1 + (rx)*y_1 +  (1+s)*z_1
	
	#Back to spherical polar coordinates from cartesian
	#Need some of the characteristics of the new ellipsoid    
	a_2, b_2 =6378137.000, 6356752.3141 #The GSR80 semi-major and semi-minor axes used for WGS84(m)
	e2_2 = 1- (b_2*b_2)/(a_2*a_2)   #The eccentricity of the GRS80 ellipsoid
	p = math.sqrt(x_2**2 + y_2**2)
	
	#Lat is obtained by an iterative proceedure:   
	lat = math.atan2(z_2,(p*(1-e2_2))) #Initial value
	latold = 2*math.pi
	while abs(lat - latold)>10**-16: 
	    lat, latold = latold, lat
	    nu_2 = a_2 / math.sqrt( 1 - e2_2 * math.sin(latold)**2)
	    lat = math.atan2( z_2 + e2_2 * nu_2 * math.sin(latold), p)
	
	#Lon and height are then pretty easy
	lon = math.atan2(y_2,x_2)
	H = p/math.cos(lat) - nu_2

	#Uncomment this line if you want to print the results
	#print [(lat-lat_1)*180/pi, (lon - lon_1)*180/pi]
	
	#Convert to degrees
	lat = math.degrees( lat )
	lon = math.degrees( lon )
	
	#Job's a good'n. 
	return ( lat, lon )



if __name__ == '__main__':

	print 'BNG-2-Location'
	
	easting 	= 0
	northing 	= 0
	
	try:
		easting  = float( sys.argv[1] )
		northing = float( sys.argv[2] )
		try:
			result = BNG2toLatLong( easting, northing )
			print 'BNG: ' + str(  (easting, northing) ) + ' -> lat,long: ' + str(result)  
		except:
			print 'Conversion error encountered'
		
	except ValueError as e:
		print 'Input error: ' + str( e )
		
