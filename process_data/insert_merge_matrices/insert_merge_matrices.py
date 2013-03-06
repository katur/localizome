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

		# first get the protein name as chars before _ in filename
		protein = filename.partition("_")[0]
		
		if protein == "F-ACTIN (GFP//MOE)":
			protein="act-1"	
		elif protein == "C18E3.2":
			protein="swsn-2.2"
		elif protein == "F33G12.3":
			protein="lrr-1"
		elif protein == "SP-12":
			protein="C34B2.10"
		elif protein == "VBP-1":
			protein="pfd-3"
		elif protein =="GBP-1":
			protein="gpb-1"
		elif protein == "ZK849.2":
			protein="gopc-1"
		print protein

		# query database to get the protein_id for the corresponding protein name
		c = db.cursor()
		num_lines = c.execute("""SELECT id FROM website_protein WHERE common_name=%s""", protein)
		if num_lines > 1:
			sys.exit("Error: too many proteins match " + protein)
		elif num_lines < 1:
			sys.exit("Error: " + protein + " not found")
		else:
			protein_id = c.fetchone()[0]
		c.close()
		print protein_id
		
		# open file and parse matrix, inserting values into db
		with open(filename, "U") as f: # open file
			data = csv.reader(f) # refresh reader to get signla data
			try:
				process_merge_matrix(data, protein_id)
			except csv.Error as e:
				sys.exit('file %s, line %d: %s' % (filename, data.line_num, e))




def process_merge_matrix(data, protein_id):
	"""
	process rows of matrix
	"""
	global db
	global timepoint_dictionary
	global compartment_dictionary

	# create a list of the timepoints in the order they are in this file
	timepoint_list = data.next()

	row = data.next() # first row of signal data
	
	# for each row, i.e. each compartment
	while row[0].strip() != "":
		compartment = row[0]
		compartment_id = compartment_dictionary[compartment]
		i=0
		for item in row[1:]:
			# calculate item code
			if item == '0':
				item = 0
			elif item == '10':
				item = 1
			elif item == '70':
				item = 2
			elif item == '100':
				item = 3
			else:
				sys.exit("Error: signal " + item + " is invalid") 

			# calculate timepoint_id
			timepoint_id = timepoint_dictionary[timepoint_list[i]]
			#c = db.cursor()
			#c.execute("""INSERT INTO website_signalmerged (strength, compartment_id, timepoint_id, protein_id) VALUES (%s, %s, %s, %s);COMMIT;""", (item, compartment_id, timepoint_id, protein_id))
			#c.close()
			i += 1
			print compartment_id + timepoint_id + item
		print "\n\n"
		row = data.next()



def create_dictionary(query):
	"""
	creates a dictionary from the first two elements returned from a select query.
	the first element is the key, the second element is the value
	"""
	# query database for two values, turning results into a dictionary
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
db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf")
	
# dictionaries for the timepoints and compartments
# timepoints are only unique per category, so create three
timepoint_dictionary = create_dictionary("""SELECT kahn_merge_name, id FROM website_timepoint""")

# compartments are unique
compartment_dictionary = create_dictionary("""SELECT miyeko_excel_name, id FROM website_compartment""")	

# run main method
main()

# close database connection
db.close()
