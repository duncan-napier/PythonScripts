#
#	airport resource reader
#

import os, sys

def usage():
	print 'Usage\n~~~~~\nairport_kml.py <airport csv file>\n'
	
def main():
	try:
		csv_file = sys.argv[1]
	except IndexError:
		usage()
		return

	output_path = os.path.basename( csv_file ) + '.kml'
	print 'Writting to file.... ' + output_path
	
if __name__ == '__main__':
	main()