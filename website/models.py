from django.db import models

# Note: blank=True means is allowed to be blank. default blank=False.
class Protein(models.Model):
	common_name = models.CharField(max_length=20, unique=True)
	sequence = models.CharField(max_length=20, unique=True)
	wormbase_id = models.CharField(max_length=20, unique=True)
	representative_video = models.OneToOneField('Video', related_name='representative', null=True) # eventually remove null=True; optionally add unique=True
	def __unicode__(self):
		return self.common_name
	class Meta:
		ordering = ['common_name']
	
	# permalink takes a URL pattern (either a view name or URL pattern) and
	# a list of arguments, and uses URLconf patters to construct URL
	@models.permalink 
	def get_absolute_url(self):
		return ('protein_detail_url', [str(self.common_name)])


class Strain(models.Model):
	name = models.CharField(max_length=10) # consider adding unique=True, but deal w/the two strains with no strain name first!
	vector = models.CharField(max_length=10, blank=True) # possibly change this field to be vector OR genotype
	protein = models.ForeignKey(Protein)
	class Meta:
		ordering = ['protein', 'name']


class Video(models.Model):
	protein = models.ForeignKey(Protein)
	strain = models.ForeignKey(Strain)
	strain_name = models.CharField(max_length=10)
	vector = models.CharField(max_length=10, blank=True)
	filename = models.CharField(max_length=40)
	movie_number = models.PositiveSmallIntegerField()
	excel_id = models.PositiveSmallIntegerField(unique=True)	
	date_filmed = models.DateField()
	date_scored = models.DateField()
	lens = models.CharField(max_length=5)
	mode = models.CharField(max_length=70)
	summary = models.CharField(max_length=2000)
	def __unicode__(self):
		return self.protein
	def shortened_filename(self):
		s = self.filename.partition('_')[2] # remove protein from beginning of string
		s = s.rpartition('_')[0] # remove date from end of string
		return s
	class Meta:
		ordering = ['movie_number']


class VideoNotes(models.Model):
	"""
	These notes seem to be redundant with summary.
	After confirmation, can remove this class entirely from the database.
	"""
	note = models.CharField(max_length=700)
	video = models.ForeignKey(Video)


class Compartment(models.Model):
	PERIPHERY_SUPERCOMPARTMENT = 1
	CYTOPLASMIC_SUPERCOMPARTMENT = 2
	NUCLEAR_SUPERCOMPARTMENT = 3
	
	SUPERCOMPARTMENT_CATEGORIES = (
		(PERIPHERY_SUPERCOMPARTMENT, 'Periphery/Plasma Membrane'),
		(CYTOPLASMIC_SUPERCOMPARTMENT, 'Cytoplasmic'),
		(NUCLEAR_SUPERCOMPARTMENT, 'Nuclear')
	)
	supercompartment = models.PositiveSmallIntegerField(choices=SUPERCOMPARTMENT_CATEGORIES)
	name = models.CharField(max_length=60, unique=True) # compartment names unique
	short_name = models.CharField(max_length=20)
	extra_short_name = models.CharField(max_length=5)
	miyeko_excel_name = models.CharField(max_length=60, unique=True) # can remove this field eventually
	display_order = models.PositiveSmallIntegerField(unique=True) # might remove this field eventually
	class Meta:
		ordering = ['display_order']


class Timepoint(models.Model):
	ONE_CELL_CYCLE = 1
	AB_CELL_CYCLE = 2
	P1_CELL_CYCLE = 3
	
	CELL_CYCLE_CATEGORIES = (
		(ONE_CELL_CYCLE, '1-Cell'),
		(AB_CELL_CYCLE, 'AB'),
		(P1_CELL_CYCLE, 'P1')
	)
	cell_cycle_category = models.PositiveSmallIntegerField(choices=CELL_CYCLE_CATEGORIES)
	name = models.CharField(max_length=30) # timepoint names are NOT unique (repeat across cell cycle categories)
	short_name = models.CharField(max_length=5)
	miyeko_excel_name = models.CharField(max_length=30) # can remove this field eventually
	kahn_merge_name = models.CharField(max_length=35) # can remove this field eventually
	display_order = models.PositiveSmallIntegerField(unique=True) # might remove this field eventually
	class Meta:
		ordering = ['display_order']


class Signal(models.Model):
	ABSENT_STRENGTH = 0
	UNKNOWN_STRENGTH = 1
	WEAK_STRENGTH = 2
	PRESENT_STRENGTH = 3
	
	STRENGTH_CATEGORIES = (
		(ABSENT_STRENGTH, 'absent'),
		(UNKNOWN_STRENGTH, 'na'),
		(WEAK_STRENGTH, 'weak'),
		(PRESENT_STRENGTH, 'present')
	)
	strength = models.PositiveSmallIntegerField(choices=STRENGTH_CATEGORIES, db_index=True)
	compartment = models.ForeignKey(Compartment)
	timepoint = models.ForeignKey(Timepoint)
	class Meta:
		abstract = True # parent class for SignalRaw and SignalMerged


class SignalRaw(Signal): # inherits fields from Signal
	video = models.ForeignKey(Video)
	class Meta:
		ordering = ['video', 'compartment', 'timepoint']


class SignalMerged(Signal): # inherits fields from Signal
	protein = models.ForeignKey(Protein)
	class Meta:
		ordering = ['protein', 'compartment', 'timepoint']
