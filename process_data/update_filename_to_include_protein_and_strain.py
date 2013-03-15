import MySQLdb
import sys
import string

def main():
	db = MySQLdb.connect(db="localizome", read_default_file="~/.my.cnf") 
	c = db.cursor()
	num_lines = c.execute(
		"""SELECT website_video.`id`, website_video.`filename`, website_protein.`common_name`, website_strain.`name` 
			FROM website_video
			LEFT JOIN website_protein ON website_video.`protein_id` = website_protein.`id`
			LEFT JOIN website_strain ON website_video.`strain_id` = website_strain.`id`
		"""
	)
	result = c.fetchall()
	c.close()

	for row in result:
		video_id = row[0]
		filename = row[1].strip()
		protein = row[2].translate(string.maketrans("",""), string.punctuation)
		strain = row[3]
		filename = protein + "_" + strain + "_" + filename
		print filename
		
		c = db.cursor()
		c.execute("""UPDATE website_video SET filename = %s WHERE id=%s;COMMIT;""", (filename, video_id))
		c.close()
	
	db.close()
		
main()
