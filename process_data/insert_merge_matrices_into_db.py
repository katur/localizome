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
	# e.g. run as python insert_merge_matrices_into_db.py ../raw_data/merge_matrices/*.table.txt 

		# first get the protein name as chars before _ in filename
		protein = filename.partition("_")[0]
		
		if protein == "F-ACTIN":
			protein="ACT-1"	
		elif protein == "SP-12":
			protein="SP12"
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

		# open file and parse matrix, inserting values into db
		with open(filename, "U") as f: # open file
			data = csv.reader(f, delimiter='\t') # refresh reader to get signal data
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
	
	# for each row, i.e. each compartment
	for row in data:
		compartment = row[0]
		if compartment == "ER":
			compartment = "endoplasmic reticulum"
		elif compartment == "microtubule-like:midzone":
			compartment = "microtubule-like: midzone"
		compartment_id = compartment_dictionary[compartment]
		i=0
		for item in row[1:]:
			# calculate item code
			if item == '0':
				item = 0
			elif item == '1':
				item = 1
			elif item == '5':
				item = 2
			elif item == '10':
				item = 3
			else:
				sys.exit("Error: signal " + item + " is invalid") 

			# calculate timepoint_id
			timepoint_id = timepoint_dictionary[timepoint_list[i]]
			c = db.cursor()
			c.execute("""INSERT INTO website_signalmerged (strength, compartment_id, timepoint_id, protein_id) VALUES (%s, %s, %s, %s);COMMIT;""", (item, compartment_id, timepoint_id, protein_id))
			c.close()
			i += 1
	print "\n\n"



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
compartment_dictionary = create_dictionary("""SELECT name, id FROM website_compartment""")	

# run main method
main()

# close database connection
db.close()
