from django.db import models

class Protein(models.Model):
	common_name = models.CharField(max_length=10, unique=True)
	sequence = models.CharField(max_length=15, unique=True)
	wormbase_id = models.CharField(max_length=15, unique=True)
	representative_video = models.OneToOneField('Video', related_name='representative', null=True, unique=True)
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
	name = models.CharField(max_length=10)
	
	# genotype is vector if miyeko's strain (to dynamically generate genotype), hard-coded if not hers and not on WormBase, blank otherwise.
	genotype = models.CharField(max_length=100, blank=True) 	
	protein = models.ForeignKey(Protein)
	note = models.CharField(max_length=75, blank=True)


class Video(models.Model):
	protein = models.ForeignKey(Protein)
	strain = models.ForeignKey(Strain)
	filename = models.CharField(max_length=30, unique=True)
	movie_number = models.PositiveSmallIntegerField()
	excel_id = models.PositiveSmallIntegerField(unique=True, null=True)
	date_filmed = models.DateField()
	date_scored = models.DateField(null=True)
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
	name = models.CharField(max_length=60, unique=True)
	short_name = models.CharField(max_length=20, blank=True) # blank indicates to not display compart.
	extra_short_name = models.CharField(max_length=5, blank=True) # when axes flip
	
	PERIPHERY_SUPERCOMPARTMENT = 1
	CYTOPLASMIC_SUPERCOMPARTMENT = 2
	NUCLEAR_SUPERCOMPARTMENT = 3
	
	SUPERCOMPARTMENT_CATEGORIES = (
		(PERIPHERY_SUPERCOMPARTMENT, 'Periphery/Plasma Membrane'),
		(CYTOPLASMIC_SUPERCOMPARTMENT, 'Cytoplasmic'),
		(NUCLEAR_SUPERCOMPARTMENT, 'Nuclear')
	)
	supercompartment = models.PositiveSmallIntegerField(choices=SUPERCOMPARTMENT_CATEGORIES)
	class Meta:
		ordering = ['id']


class Timepoint(models.Model):
	name = models.CharField(max_length=30) # timepoint names NOT unique (depend on cell cycle)
	short_name = models.CharField(max_length=5)
	kahn_merge_name = models.CharField(max_length=35) # can remove eventually
	
	ONE_CELL_CYCLE = 1
	AB_CELL_CYCLE = 2
	P1_CELL_CYCLE = 3
	
	CELL_CYCLE_CATEGORIES = (
		(ONE_CELL_CYCLE, '1-Cell'),
		(AB_CELL_CYCLE, 'AB'),
		(P1_CELL_CYCLE, 'P1')
	)
	cell_cycle_category = models.PositiveSmallIntegerField(choices=CELL_CYCLE_CATEGORIES)
	class Meta:
		ordering = ['id']


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
