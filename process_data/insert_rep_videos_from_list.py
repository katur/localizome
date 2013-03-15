import MySQLdb
import csv
import sys

def main():
	"""
	as first arg in console, pass 
		/path/filename.csv
	"""
	global db	

	# open file and parse matrix, inserting values into db
	with open(sys.argv[1], 'r') as f: # open file
		data = csv.reader(f)
		try:
			process_video_list(data)
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, data.line_num, e))




def process_video_list(data):
	"""
	process rows
	"""
	global db

	# for each row, i.e. each compartment
	for row in data:
		filename = row[0].strip()

		c = db.cursor()
		c.execute("""SELECT id, protein_id FROM website_video WHERE filename = (%s);""", (filename))
		result = c.fetchone()
		video_id = result[0]
		protein_id = result[1]
		c.close()

		c = db.cursor()
		c.execute("""UPDATE website_protein SET representative_video_id = (%s) WHERE id = (%s);COMMIT;""", (video_id, protein_id))
		c.close()


############################
# RUN PROGRAM
############################
#global variables
db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf")
	
# run main method
main()

# close database connection
db.close()
