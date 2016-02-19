import csv, json, sys, os



def main():
	input_path = sys.argv[1]
	input = open(input_path)
	data = json.load(input)
	input.close()
	
	
	output_path = os.path.basename(input_path) + '.csv'
	print "Writing file " + output_path
	
	
	out_file = open(output_path, 'wb')
	output = csv.writer(out_file)
	
	output.writerow(data[0].keys())  # header row
	
	for row in data:
		output.writerow(row.values())
		
		if row['changed_method'] != None:
			print 'Changed_method  = ' + str( row['changed_method'] )
	
	out_file.close()
	
	
if __name__ == '__main__':
	main()