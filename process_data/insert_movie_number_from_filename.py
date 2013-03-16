import MySQLdb
import sys
import string

def main():
	db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf") 
	c = db.cursor()
	num_lines = c.execute(
		"""SELECT website_video.`id`, website_video.`filename` 
			FROM website_video;
		"""
	)
	result = c.fetchall()
	c.close()

	for row in result:
		video_id = row[0]
		filename = row[1].strip()
		filename = filename.rpartition("_")[0] # remove date from end of filename
		filename = filename.rpartition("_")[2] # extract movie number from end of remaining filename
		print filename
		
		c = db.cursor()
		c.execute("""UPDATE website_video SET movie_number = %s WHERE id=%s;COMMIT;""", (filename, video_id))
		c.close()
	
	db.close()
		
main()
