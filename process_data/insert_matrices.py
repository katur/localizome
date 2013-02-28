import MySQLdb
import csv
import sys

def main():
	"""
	as first arg in console, pass 
		/path/*.csv 
	to process ALL csvs in a directory
	"""
	global db	
	
	for filename in sys.argv[1:]: # for each file matching args[1]
		with open(filename, "U") as f: # open file; "U" helps with EOF format
			data = csv.reader(f) # create reader to get video meta data
			try:
				video_id = add_video_meta_to_db(data, filename)
			except csv.Error as e:
				sys.exit('file %s, line %d: %s' % (filename, data.line_num, e))

		with open(filename, "U") as f: # open file again
			data = csv.reader(f) # refresh reader to get signla data
			try:
				process_matrix(data, video_id)
			except csv.Error as e:
				sys.exit('file %s, line %d: %s' % (filename, data.line_num, e))
	

def add_video_meta_to_db(data, filename):
	"""
	process rows of video meta data at bottom of csv
	"""
	global max_summary_length
	global max_note_length
	global db

	# first get the excel_id as number before . in filename
	excel_id = filename.partition(".")[0]
	if not is_number(excel_id):
		sys.exit("Error: file " + filename + " is not a number")

	# skip matrix rows
	row = data.next()
	while row[0].strip() != "PROTEIN:":
		row = data.next()
	
	notes = [] # list for notes (variable number of notes)
	i = 0 # counter for notes

	# traverse the video meta information, extracting variables needed for db
	while True:
		# for these rows, just collect value
		if row[0].strip() == "PROTEIN:":	
			protein=row[1]
		elif row[0].strip() == "LINE:":
			strain=row[1]
		elif row[0].strip() == "VECTOR:":
			vector=row[1]
		elif row[0].strip() == "MOVIE:":
			movie=row[1]
		elif row[0].strip() == "Lens:":
			lens=row[1]
		elif row[0].strip() == "Mode:":
			mode=row[1]
		
		# for date, deal with format 112013 or 81013
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
		
		# for notes and summary, deal with multiples and char length
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
		
		# if abnormalities
		elif row[1].strip() == "":
			print "Warning: skipping a row in " + excel_id
		else:
			sys.exit("Error: formatting errors in " + excel_id)
		
		# end loop when reach summary
		if row[0].strip() == "SUMMARY:":
			break
		row = data.next()

	# query database to get the protein_id for the corresponding protein name
	c = db.cursor()
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
	c.close()

	# insert a row per note into the database
	for note in notes:
		c = db.cursor()
		c.execute("""INSERT INTO website_videonotes (note, video_id) VALUES (%s, %s);COMMIT;""", (note, video_id))
		c.close()
	
	# return video_id, which is needed to parse the matrix
	return video_id



def process_matrix(data, video_id):
	"""
	process rows of matrix
	"""
	global db
	global timepoint_dictionary
	global compartment_dictionary

	data.next() #skip the "Time" header row
	data.next() #skip the cell-division cycle row (e.g., "1-cell")

	# create a list of the timepoints in the order they are in this file
	timepoint_list = data.next() # timepoints[0:1] are empty
	data.next() #skip the periphery/plasma membrane row

	row = data.next() # first row of signal data
	
	# for each row, i.e. each compartment
	while row[1].strip() != "":
		if row[1].strip() == "cytoplasmic" or row[1].strip() == "nuclear":
			row = data.next()
			continue
		compartment = row[1]
		compartment_id = compartment_dictionary[compartment]
		i=2
		for item in row[2:22]:
			# calculate item code
			item = item.strip().partition("*")[0]
			if item == '0':
				item = 0
			elif item == 'na':
				item = 1
			elif item == 'w':
				item = 2
			elif item == '1':
				item = 3
			else:
				sys.exit("Error: signal " + item + " is invalid") 

			# calculate timepoint_id
			if i<=9:
				timepoint_id = timepoint_dictionary_1[timepoint_list[i]]
			elif i<=15:
				timepoint_id = timepoint_dictionary_2[timepoint_list[i]]
			else:
				timepoint_id = timepoint_dictionary_3[timepoint_list[i]]
			c = db.cursor()
			c.execute("""INSERT INTO website_signalraw (strength, compartment_id, timepoint_id, video_id) VALUES (%s, %s, %s, %s);COMMIT;""", (item, compartment_id, timepoint_id, video_id))
			c.close()
			i += 1
		row = data.next()



def create_dictionary(query):
	"""
	creates a dictionary from the first two elements returned from a select query.
	the first element is the key, the second element is the value
	"""
	# query database for the timepoints, turning results into a dictionary
	dictionary = {}
	c = db.cursor()
	c.execute(query)
	result = c.fetchall()
	for row in result:
		dictionary[row[0]] = row[1] # key: 0th element; value: 1st element
	c.close()
	return dictionary



def is_number(s):
	"""
	check if a string is a number
	"""
	try:
		float(s)
		return True
	except ValueError:
		return False



############################
# RUN PROGRAM
############################

#global variables
max_summary_length = 0;
max_note_length = 0;
db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf")
	
# dictionaries for the timepoints and compartments
# timepoints are only unique per category, so create three
timepoint_dictionary_1 = create_dictionary("""SELECT miyeko_excel_name, id FROM website_timepoint WHERE cell_cycle_category=1""")
timepoint_dictionary_2 = create_dictionary("""SELECT miyeko_excel_name, id FROM website_timepoint WHERE cell_cycle_category=2""")
timepoint_dictionary_3 = create_dictionary("""SELECT miyeko_excel_name, id FROM website_timepoint WHERE cell_cycle_category=3""")

# compartments are unique
compartment_dictionary = create_dictionary("""SELECT miyeko_excel_name, id FROM website_compartment""")	

# run main method
main()

# close database connection
db.close()

# print results to apply to database schema
print "max summary length is " + str(max_summary_length)
print "max note length is " + str(max_note_length)
