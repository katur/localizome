import MySQLdb
import csv
def main():
	# connect to database
	db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf")
	c = db.cursor() # create a cursor to execute queries on
	query = """SELECT * FROM website_protein"""
	num_lines = c.execute(query)
	print num_lines
	while True:
		row = c.fetchone() # fetch one row
		if row == None:
			break		
		print row
	
	# read the data from the csv
	data = csv.reader(open('data.csv', "U")) # "U" helps with end-of-line format
	data.next() #skip the "Time" header row
	data.next() #skip the cell-division cycle row (e.g., "1-cell")

	# create a list of the timepoints from the timepoint row
	timepoints = data.next() # timepoints[0:1] are empty
	
	# traverse rows of signal data
	data.next() #skip the periphery/plasma membrane row
	process_rows_until("cytoplasmic", data, timepoints)
	process_rows_until("nuclear", data, timepoints)
	process_rows_until("", data, timepoints)
	
	# close database connection
	db.close()

def process_rows_until(stop_signal, data, timepoints):
	"""
	process rows of signals until reaching an invalid signal row
	"""
	row = data.next()
	while row[1] != stop_signal:
		compartment = row[1]
		print compartment
		i = 2
		for item in row[2:21]:
			print timepoints[i], item
			i += 1
		row = data.next()
		print '\n'
	print "reached", stop_signal

main()
