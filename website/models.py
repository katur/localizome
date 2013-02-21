from django.db import models

# Note: blank=True means is allowed to be blank. False is default.
class Protein(models.Model):
	common_name = models.CharField(max_length=20)
	sequence = models.CharField(unique=True, max_length=20)
	wormbase_id = models.CharField(max_length=20, blank=True)
	def __unicode__(self):
		return self.common_name
	@models.permalink 
	# permalink takes a URL pattern (either a view name or URL pattern),
	# and a list of arguments, and uses URLconf patters to construct URL
	def get_absolute_url(self):
		return ('protein_detail_url', [str(self.common_name)])
	class Meta:
		ordering = ['common_name']

class Video(models.Model):
	date_filmed = models.DateField(blank=True)
	protein = models.ForeignKey(Protein)
	lens = models.CharField(max_length=50, blank=True)
	notes = models.CharField(max_length=200, blank=True)
	def __unicode__(self):
		return self.protein

class Compartment(models.Model):
	compartment_name = models.CharField(max_length=50)
	display_order = models.PositiveSmallIntegerField()

class Timepoint(models.Model):
	CELL_CYCLE_CATEGORIES = (
		(u'1', u'1-cell'),
		(u'2', u'AB'),
		(u'3', u'P1')
	)
	cell_cycle_category = models.PositiveSmallIntegerField(choices=CELL_CYCLE_CATEGORIES)
	timepoint_name = models.CharField(max_length=50)
	display_order = models.PositiveSmallIntegerField()

class SignalCommonInfo(models.Model):
	STRENGTH_CATEGORIES = (
		(u'0', u'no data'),
		(u'1', u'not present'),
		(u'2', u'weak'),
		(u'3', u'present')
	)
	strength = models.PositiveSmallIntegerField(choices=STRENGTH_CATEGORIES)
	compartment = models.ForeignKey(Compartment)
	timepoint = models.ForeignKey(Timepoint)
	class Meta:
		abstract = True # parent fields for SignalRaw and SignalMerged

class SignalRaw(SignalCommonInfo): # inherits fields from SignalCommonInfo
	video = models.ForeignKey(Video)

class SignalMerged(SignalCommonInfo): # inherits fields from SignalCommonInfo
	protein = models.ForeignKey(Protein)
