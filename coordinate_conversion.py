
import math

#Datum	Equatorial Radius, meters (a)	Polar Radius, meters (b)	Flattening (a-b)/a	=
datum_WGS84 = [ 'NAD83/WGS84', 6378137.0, 6356752.3142, 298.257223563 ]
datum_GRS80 = [ 'GRS 80', 6378137.0, 6356752.3141, 298.257222101 ]
datum_WGS72 = [ 'WGS72', 6378135.0, 6356750.5, 298.26 ]
datum_Australian = [ 'Australian 1965', 6378160.0, 6356774.7, 298.25 ]
datum_Krasovsky = [ 'Krasovsky 1940', 6378245.0, 6356863.0, 298.3 ]
datum_International = [ 'International (1924) -Hayford (1909)', 6378388.0, 6356911.9, 297 ]
datum_Clark = [ 'Clake 1880', 6378249.1, 6356514.9, 293.46 ]
datum_Clarke = [ 'Clarke 1866', 6378206.4, 6356583.8, 294.98 ]
datum_Airy = [ 'Airy 1830', 6377563.4, 6356256.9, 299.32 ]
datum_Bessel = [ 'Bessel 1841', 6377397.2, 6356079.0, 299.15 ]
datum_Everest = [ 'Everest 1830', 6377276.3, 6356075.4, 300.80 ]





# Symbols as used in USGS PP 1395: Map Projections - A Working Manual
datum_list = [ datum_WGS84, datum_GRS80, datum_WGS72, datum_Australian, datum_International, datum_Clark, datum_Clarke, datum_Airy, datum_Bessel, datum_Everest ]

#DatumEqRad = [6378137.0,6378137.0,6378137.0,6378135.0,6378160.0,6378245.0,6378206.4, 6378388.0,6378388.0,6378249.1,6378206.4,6377563.4,6377397.2,6377276.3]
#DatumFlat  = [298.2572236, 298.2572236, 298.2572215, 298.2597208, 298.2497323, 298.2997381, 294.9786982, 296.9993621, 296.9993621, 293.4660167, 294.9786982, 299.3247788, 299.1527052, 300.8021499]

Item = 0 		# Default
k0 = 0.9996		# scale on central meridian
a = datum_list[Item][1] 	# equatorial radius, meters. 
f = 1/datum_list[Item][3] 	# polar flattening.
b = a*(1-f)					# polar axis.
e = math.sqrt(1 - float(b*b)/(a*a))	# eccentricity


drad = math.pi/180 # Convert degrees to radians)
#latd = 0;//latitude in degrees
#phi = 0;//latitude (north +, south -), but uses phi in reference
#e0 = e/Math.sqrt(1 - e*e);//e prime in reference
#N = a/Math.sqrt(1-Math.pow(e*Math.sin(phi)),2);
#T = Math.pow(Math.tan(phi),2);
#C = Math.pow(e*Math.cos(phi),2);
#lng = 0;//Longitude (e = +, w = -) - can't use long - reserved word
#lng0 = 0;//longitude of central meridian
#lngd = 0;//longitude in degrees
#M = 0;//M requires calculation
#x = 0;//x coordinate
#y = 0;//y coordinate
#k = 1;//local scale
utmz = 15 #utm zone
#zcm = 0;//zone central meridian
#OOZok = false;



	
def UTMtoGeog( easting, northing, southOfEquator = False, zone = utmz ):
	'''Convert Latitude and Longitude to UTM'''
	
	print 'Converting (' + str( easting ) + ', ' + str(northing) + ')'
	
	e0 = e / math.sqrt(1 - e*e)	# Called e prime in reference
	esq = (1 - (b/a)*(b/a) )	# e squared for use in expansions
	e0sq = e*e/(1-e*e)			# e0 squared - always even powers
	x = easting
	#if x < 160000 or x > 840000:
	#	raise RunTimeError( 'Outside permissible range of easting values \n Results may be unreliable \n Use with caution' 
	y = northing
	
	if y < 0:
		raise RunTimeError( 'Negative values not allowed.\nResults may be unreliable.\nUse with caution' )
	elif y > 10000000:
		raise RunTimeError( 'Northing may not exceed 10,000,000.\nResults may be unreliable.\nUse with caution' )
		

	#utmz = parseFloat(document.getElementById("UTMzBox1").value);
	zcm = 3 + 6*(utmz-1) - 180 # Central meridian of zone
	e1 = (1 - math.sqrt(1 - e*e))/(1 + math.sqrt(1 - e*e))	# Called e1 in USGS PP 1395 also
	M0 = 0.0		# In case origin other than zero lat - not needed for standard UTM
	M = M0 + y/k0	# Arc length along standard meridian. 
	if southOfEquator:
		M = M0 + float(y-10000000)/k
	mu = M/(a*(1 - esq*(1/4 + esq*(3/64 + 5*esq/256))))
	phi1 = mu + e1*(3/2 - 27*e1*e1/32)*math.sin(2*mu) + e1*e1*(21/16 -55*e1*e1/32)*math.sin(4*mu) # Footprint Latitude
	phi1 = phi1 + e1*e1*e1*(math.sin(6*mu)*151/96 + e1*math.sin(8*mu)*1097/512)
	C1 = e0sq*math.pow(math.cos(phi1),2)
	T1 = math.pow(math.tan(phi1),2)
	N1 = a/math.sqrt(1-math.pow(e*math.sin(phi1),2))
	R1 = N1*(1-e*e)/(1-math.pow(e*math.sin(phi1),2))
	D = (x-500000)/(N1*k0)
	phi = (D*D)*(1/2 - D*D*(5 + 3*T1 + 10*C1 - 4*C1*C1 - 9*e0sq)/24)
	phi = phi + math.pow(D,6)*(61 + 90*T1 + 298*C1 + 45*T1*T1 -252*e0sq - 3*C1*C1)/720
	phi = phi1 - (N1*math.tan(phi1)/R1)*phi
	
	# Output Latitude
	latitude = math.floor(1000000*phi/drad)/1000000
	# Output Longitude
	lng = D*(1 + D*D*((-1 -2*T1 -C1)/6 + D*D*(5 - 2*C1 + 28*T1 - 3*C1*C1 +8*e0sq + 24*T1*T1)/120))/math.cos(phi1)
	lngd = zcm+lng/drad
	longitude = math.floor(1000000*lngd)/1000000
	
	data = ( latitude, longitude )
	print ' lat, long = ' + str (  data )
	return data



if __name__=='__main__':
	coord = UTMtoGeog( 1548706.792, 8451449.199 )
	print 'Converted values : ' + str( coord )
	
	expected_lat_long = ( 70.57927709, 	45.59941973 )
