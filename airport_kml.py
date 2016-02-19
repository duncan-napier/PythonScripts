#
#	airport resource reader
#


import os, sys

# how to use this script
def usage():
	print 'Usage\n~~~~~\nairport_kml.py <airport csv file>\n'
	
# main function
def main():
	try:
		csv_file = sys.argv[1]
	except IndexError:
		usage()
		return

	output_path = os.path.basename( csv_file ) + '.kml'
	print 'Writting to file.... ' + output_path
	
# entry point to the script
if __name__ == '__main__':
	main()