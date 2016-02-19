	
	
from math import radians, sin, cos, acos, atan2, sqrt, pow


def calculateTrueDistance( from_lat, from_long, to_lat, to_long ):
	R = 6371000 # meters
	phi_1 = radians( from_lat )
	phi_2 = radians( to_lat )
	phi_delta = radians( to_lat - from_lat )
	lambda_delta = radians( to_long - from_long )
	
	a =  pow( sin( 0.5*phi_delta ), 2 ) + cos( phi_1 ) * cos( phi_2 ) * pow( sin( 0.5*lambda_delta ), 2 )
	c = 2 * atan2( sqrt(a), sqrt(1-a) )
	d = R * c
	
	#d = acos( sin( phi_1 )*sin(phi_2)+cos(phi_1)*cos(phi_2)*cos(lambda_delta) ) * R
	return d
	
	
	
#def main():
#	print "Calculating distance!"
#	
#	x0 = 41.407527734
#	y0 = 2.1626958847
#	x1 = 41.4059906006
#	y1 = 2.16314697266
#	
#	dist = calculateTrueDistance( x0, y0, x1, y1 )
#	
#	print "From (" + str(x0) + "," + str(y0) + ") to (" + str(x1) + "," + str(y1) + ") = " + str( dist ) + "m"
#	 
#if __name__== "__main__":
#	main()	