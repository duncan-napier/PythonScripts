
import datetime
import dateutil.parser

def main():
	print "DateTime Tests"
	
	text = '2015-09-18T09:03:59.654'
	
	DT = dateutil.parser.parse( text );
	print "Time: " + str( DT ) + "(" + DT.isoformat()  + ")"
	

if __name__=='__main__':
	main()