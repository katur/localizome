from django.db import models

# Note: blank=True means is allowed to be blank. False is default.
class Protein(models.Model):
	common_name = models.CharField(max_length=20)
	sequence = models.CharField(unique=True, max_length=20)
	wormbase_id = models.CharField(max_length=20, blank=True)
	representative_video = models.OneToOneField('Video', related_name='representative', null=True)
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
	protein = models.ForeignKey(Protein)
	strain = models.CharField(max_length=20, blank=True)
	vector = models.CharField(max_length=20, blank=True)
	filename = models.CharField(max_length=50, blank=True)
	excel_id = models.PositiveSmallIntegerField(null=True)	
	date_filmed = models.DateField(null=True)
	lens = models.CharField(max_length=50, blank=True)
	mode = models.CharField(max_length=200, blank=True)
	summary = models.CharField(max_length=5000, blank=True)
	def __unicode__(self):
		return self.protein

class VideoNotes(models.Model):
	note = models.CharField(max_length=2000)
	video = models.ForeignKey(Video)

class Compartment(models.Model):
	SUPERCOMPARTMENT_CATEGORIES = (
		(u'1', u'periphery/plasma membrane'),
		(u'2', u'cytoplasmic'),
		(u'3', u'nuclear')
	)
	supercompartment = models.PositiveSmallIntegerField(choices=SUPERCOMPARTMENT_CATEGORIES)
	name = models.CharField(max_length=60)
	short_name = models.CharField(max_length=20)
	miyeko_excel_name = models.CharField(max_length=60, blank=True)
	display_order = models.PositiveSmallIntegerField(unique=True)
	class Meta:
		ordering = ['display_order']

class Timepoint(models.Model):
	CELL_CYCLE_CATEGORIES = (
		(u'1', u'1-cell'),
		(u'2', u'AB'),
		(u'3', u'P1')
	)
	cell_cycle_category = models.PositiveSmallIntegerField(choices=CELL_CYCLE_CATEGORIES)
	name = models.CharField(max_length=30)
	short_name = models.CharField(max_length=5)
	miyeko_excel_name = models.CharField(max_length=30, blank=True)
	display_order = models.PositiveSmallIntegerField(unique=True)
	class Meta:
		ordering = ['display_order']

class Signal(models.Model):
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

class SignalRaw(Signal): # inherits fields from Signal
	video = models.ForeignKey(Video)
#	hello = models.CharField(max_length=10, blank=True)

class SignalMerged(Signal): # inherits fields from Signal
	protein = models.ForeignKey(Protein)
