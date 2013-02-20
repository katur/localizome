from django.db import models

# Create your models here.

# Note: blank=True means is allowed to be blank. False is default.
class Protein(models.Model):
	common_name = models.CharField(max_length=20)
	sequence = models.CharField(unique=True, max_length=20)
	wormbase_id = models.CharField(max_length=20, blank=True)
	
	def __unicode__(self):
		return self.common_name
	
	@models.permalink
	def get_absolute_url(self):
		return ('protein_detail_url', [str(self.common_name)])
	

class Video(models.Model):
	date_filmed = models.DateTimeField()
	protein = models.ForeignKey(Protein)
	lens = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.protein

