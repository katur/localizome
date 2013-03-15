from django.db import models

# Note: blank=True means is allowed to be blank. False is default.
class Protein(models.Model):
	common_name = models.CharField(max_length=20, unique=True)
	sequence = models.CharField(max_length=20, unique=True)
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


class Strain(models.Model):
	name = models.CharField(max_length=10)
	vector = models.CharField(max_length=10, blank=True)
	protein = models.ForeignKey(Protein)
	class Meta:
		ordering = ['protein', 'name']

class Video(models.Model):
	protein = models.ForeignKey(Protein)
	strain = models.ForeignKey(Strain, null=True)
	strain_name = models.CharField(max_length=10, blank=True)
	vector = models.CharField(max_length=10, blank=True)
	filename = models.CharField(max_length=40)
	excel_id = models.PositiveSmallIntegerField(unique=True)	
	date_filmed = models.DateField()
	date_scored = models.DateField()
	lens = models.CharField(max_length=5)
	mode = models.CharField(max_length=70)
	summary = models.CharField(max_length=2000)
	def __unicode__(self):
		return self.protein
	def get_filename_without_protein_or_date(self):
		short_filename = filename.partition('_')[2] # remove protein from beginning of string
		short_filename = filename.rpartition('_')[0] # remove date from end of string
		return short_filename
	class Meta:
		ordering = ['protein', 'filename']


class VideoNotes(models.Model):
	note = models.CharField(max_length=700)
	video = models.ForeignKey(Video)


class Compartment(models.Model):
	SUPERCOMPARTMENT_CATEGORIES = (
		(1, 'Periphery/Plasma Membrane'),
		(2, 'Cytoplasmic'),
		(3, 'Nuclear')
	)
	supercompartment = models.PositiveSmallIntegerField(choices=SUPERCOMPARTMENT_CATEGORIES)
	name = models.CharField(max_length=60, unique=True)
	short_name = models.CharField(max_length=20)
	extra_short_name = models.CharField(max_length=5)
	miyeko_excel_name = models.CharField(max_length=60, unique=True)
	display_order = models.PositiveSmallIntegerField(unique=True)
	class Meta:
		ordering = ['display_order']


class Timepoint(models.Model):
	CELL_CYCLE_CATEGORIES = (
		(1, '1-Cell'),
		(2, 'AB'),
		(3, 'P1')
	)
	cell_cycle_category = models.PositiveSmallIntegerField(choices=CELL_CYCLE_CATEGORIES)
	name = models.CharField(max_length=30)
	short_name = models.CharField(max_length=5)
	miyeko_excel_name = models.CharField(max_length=30, blank=True)
	kahn_merge_name = models.CharField(max_length=35, blank=True)
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
	strength = models.PositiveSmallIntegerField(choices=STRENGTH_CATEGORIES, db_index=True)
	compartment = models.ForeignKey(Compartment)
	timepoint = models.ForeignKey(Timepoint)
	class Meta:
		abstract = True # parent fields for SignalRaw and SignalMerged


class SignalRaw(Signal): # inherits fields from Signal
	video = models.ForeignKey(Video)
	class Meta:
		ordering = ['video', 'compartment', 'timepoint']


class SignalMerged(Signal): # inherits fields from Signal
	protein = models.ForeignKey(Protein)
	class Meta:
		ordering = ['protein', 'compartment', 'timepoint']
