from django.db import models

# Create your models here.

class Protein(models.Model):
	common_name = models.CharField(max_length=20)
	sequence = models.CharField(unique=True, max_length=20)
	wormbase_id = models.CharField(max_length=20)
	def __unicode__(self):
		return self.common_name

class Video(models.Model):
	date_filmed = models.DateTimeField()
	protein = models.ForeignKey(Protein)
	lens = models.CharField(max_length=50)
	def __unicode__(self):
		return self.protein

