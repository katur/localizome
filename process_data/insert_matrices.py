import MySQLdb
import csv
import sys
def main():
	"""
	as first arg in console, pass 
		/path/*.csv 
	to process ALL csvs in a directory
	"""
	# connect to database
	db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf")
	c = db.cursor() # create a cursor to execute queries on
	
	for filename in sys.argv[1:]:	
		# read the data from the csv, first to get video meta data
		data = csv.reader(open(filename, "U")) # "U" helps with end-of-line format
		add_video_meta_to_db(data, c)
	
	for filename in sys.argv[1:]:
		# read the data from the csv, this time to get the signal data
		data = csv.reader(open(filename, "U"))
		data.next() #skip the "Time" header row
		data.next() #skip the cell-division cycle row (e.g., "1-cell")

		# create a list of the timepoints from the timepoint row
		timepoints = data.next() # timepoints[0:1] are empty
	
		# traverse rows of signal data
		data.next() #skip the periphery/plasma membrane row
		process_rows_until("cytoplasmic", data, timepoints, c)
		process_rows_until("nuclear", data, timepoints, c)
		process_rows_until("", data, timepoints, c)
		
	# close database connection
	db.close()

def add_video_meta_to_db(data, c):
	"""
	process rows of video meta data at bottom of page
	"""
	# first skip the matrix
	row = data.next()
	while row[0].strip() != "PROTEIN:":
		row = data.next()
	
	i = 0 # counter for notes
	note = []

	while True:
		if row[0].strip() == "PROTEIN:":	
			protein=row[1]
		elif row[0].strip() == "LINE:":
			strain=row[1]
		elif row[0].strip() == "VECTOR:":
			vector=row[1]
		elif row[0].strip() == "MOVIE:":
			movie=row[1]
		elif row[0].strip() == "Date scored:":
			date=row[1]
		elif row[0].strip() == "Lens:":
			lens=row[1]
		elif row[0].strip() == "Mode:":
			mode=row[1]
		elif row[0][0:4] == "Note":
			if row[1].strip() != "":
				note.append(1)
		elif row[0].strip() == "SUMMARY:":
			summary=row[1]
		elif row[1].strip() == "":
			print "skipping a row"
		else:
			print "formatting errors"
		
		if row[0].strip() == "SUMMARY:":
			break
		row = data.next()
	num_lines = c.execute("""SELECT id FROM website_protein WHERE common_name=%s""", (protein.lower()))
	if num_lines > 1:
		print "too many proteins match"
	elif num_lines < 1:
		print "too few proteins match"
	else:
		protein_id = c.fetchone()[0]
		print protein_id
	c.execute("""INSERT INTO website_video (protein_id, strain, lens, mode, filename, summary, date_filmed) VALUES (%s, %s, %s, %s, %s, %s, %s);COMMIT;""", (protein_id, strain, lens, mode, movie, summary, date))
			

def process_rows_until(stop_signal, data, timepoints, c):
	"""
	process rows of signals until reaching an invalid signal row
	"""
	row = data.next()
	while row[1].strip() != stop_signal:
		compartment = row[1]
#		print compartment
		i = 2
		for item in row[2:21]:
#			print timepoints[i], item
			i += 1
		row = data.next()
#		print '\n'
	print "reached", stop_signal

main()
