import MySQLdb
import csv
import sys

max_summary_length = 0;
max_note_length = 0;

def main():
	"""
	as first arg in console, pass 
		/path/*.csv 
	to process ALL csvs in a directory
	"""
	# connect to database
	db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf")
	
	# for each file in the directory
	for filename in sys.argv[1:]:
		# open file
		with open(filename, "U") as f:
			# read the data, first to get video meta data
			data = csv.reader(f) # "U" helps with end-of-line format
			try:
				add_video_meta_to_db(db, data, filename)
			except csv.Error as e:
				sys.exit('file %s, line %d: %s' % (filename, data.line_num, e))
		
		with open(filename, "U") as f:
			# refresh the reader, this time to get the signal data
			c = db.cursor()
			data = csv.reader(f)
			try:
				data.next() #skip the "Time" header row
				data.next() #skip the cell-division cycle row (e.g., "1-cell")

				# create a list of the timepoints from the timepoint row
				timepoints = data.next() # timepoints[0:1] are empty
	
				# traverse rows of signal data
				data.next() #skip the periphery/plasma membrane row
				process_matrix(c, data, timepoints)
			except csv.Error as e:
				sys.exit('file %s, line %d: %s' % (filename, data.line_num, e))
		
	# close database connection
	db.close()

def add_video_meta_to_db(db, data, filename):
	"""
	process rows of video meta data at bottom of page
	"""
	global max_summary_length
	global max_note_length
	# first get the excel_id as the number before the . in the filename
	excel_id = filename.partition(".")[0]
	if not is_number(excel_id):
		sys.exit("Error: file " + filename + " is not a number")

	# first skip the matrix
	row = data.next()
	while row[0].strip() != "PROTEIN:":
		row = data.next()
	
	i = 0 # counter for notes
	notes = [] # list for notes (variable number of notes)

	# traverse the video meta information, extracting variables needed for db
	while True:
		if row[0].strip() == "PROTEIN:":	
			protein=row[1]
		elif row[0].strip() == "LINE:":
			strain=row[1]
		elif row[0].strip() == "VECTOR:":
			vector=row[1]
		elif row[0].strip() == "MOVIE:":
			movie=row[1]
		
		# Miyeko's dates currently in format 121013 or 81013
		elif row[0].strip() == "Date scored:":
			date=row[1]
			if date[0:1] == "1":
				month=date[0:2]
				day=date[2:4]
				year="20"+date[4:6]
			elif date[0:1] == "0":
				sys.exit("Error: date that starts with 0 in " + excel_id)
			else:
				month="0" + date[0:1]
				day=date[1:3]
				year="20"+date[3:5]
			if int(month)>12 or int(day)>31 or int(year)>2013:
				sys.exit("Error: improperly formatted date in " + excel_id)
			date = year + "-" + month + "-" + day
		
		elif row[0].strip() == "Lens:":
			lens=row[1]
		elif row[0].strip() == "Mode:":
			mode=row[1]
		
		elif row[0][0:4] == "Note":
			if row[1].strip() != "":
				notes.append(row[1].strip())
				if len(row[1]) >= 2000:
					sys.exit("Error: note too long in " + excel_id)
				if len(row[1]) > max_note_length:
					max_note_length = len(row[1])
		elif row[0].strip() == "SUMMARY:":
			summary=row[1]
			if len(summary) >= 5000:
				sys.exit("Error: summary too long in " + excel_id)
			if len(summary) > max_summary_length:
				max_summary_length = len(summary)
		
		elif row[1].strip() == "":
			print "Warning: skipping a row in " + excel_id
		else:
			sys.exit("Error: formatting errors in " + excel_id)
		
		# end loop when reach summary
		if row[0].strip() == "SUMMARY:":
			break
		row = data.next()
	
	# query database to get the protein_id for the corresponding protein name
	c = db.cursor() # create a cursor to execute queries on
	num_lines = c.execute("""SELECT id FROM website_protein WHERE common_name=%s""", (protein.lower()))
	if num_lines > 1:
		sys.exit("Error: too many proteins match in " + excel_id)
	elif num_lines < 1:
		sys.exit("Error: no protein match in " + excel_id)
	else:
		protein_id = c.fetchone()[0]
	c.close()

	# insert a row into db with all video information
	c = db.cursor()
	num_lines = c.execute("""INSERT INTO website_video (protein_id, excel_id, strain, vector, lens, mode, filename, summary, date_filmed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);COMMIT;""", (protein_id, excel_id, strain, vector, lens, mode, movie, summary, date))
	if num_lines != 1:
		sys.exit("Error: Inserting the video into the database failed in " + excel_id)
	c.close()

	# query db for the newly-formed video_id
	c = db.cursor()
	num_lines = c.execute("""SELECT id FROM website_video WHERE excel_id=%s""", (excel_id))
	if num_lines > 1:
		sys.exit("Error: too many videos match in " + excel_id)
	elif num_lines < 1:
		sys.exit("Error: no videos match in " + excel_id)
	else:
		video_id = c.fetchone()[0]
	print video_id
	c.close()

	# insert a row per note into the database
	for note in notes:
		c = db.cursor()
		c.execute("""INSERT INTO website_videonotes (note, video_id) VALUES (%s, %s);COMMIT;""", (note, video_id))
		c.close()


def process_matrix(c, data, timepoints):
	"""
	process rows of matrix
	"""
	row = data.next()
	while row[1].strip() != "":
		if row[1].strip() == "cytoplasmic" or row[1].strip() == "nuclear":
			row = data.next()
			continue
		compartment = row[1]
#		print compartment
		i = 2
		for item in row[2:21]:
	#		print timepoints[i], item
			i += 1
		row = data.next()
	#	print '\n'
	print "reached end of matrix"

# check if string is a number
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


# run main method
main()
print "max summary length is " + str(max_summary_length)
print "max note length is " + str(max_note_length)
