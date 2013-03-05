import MySQLdb
import sys

def main():
	db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf") 
	c = db.cursor()
	num_lines = c.execute("""SELECT id,filename FROM website_video""")
	result = c.fetchall()
	c.close()

	for row in result:
		video_id = row[0]
		filename = row[1].strip()
		date = filename.rpartition('_')[2]
		month = date[0:2]
		day = date[2:4]
		year = "20"+date[4:6]
		date = year + "-" + month + "-" + day
		print date
		c = db.cursor()
		c.execute("""UPDATE website_video SET date_filmed = %s WHERE id=%s;COMMIT;""", (date, video_id))
		c.close()
	
	db.close()
		
main()
