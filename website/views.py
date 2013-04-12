from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes context, renders
from django.db.models import Q # enables AND and OR in SQL filters
from website.models import *

def home(request):
	"""
	Homepage
	"""
	# render page
	return render_to_response('home.html', context_instance=RequestContext(request))


def protein_list(request):
	"""
	Page listing all proteins tested
	"""
	# get all proteins
	p = Protein.objects.all()

	# render page
	return render_to_response('protein_list.html', {'proteins':p}, context_instance=RequestContext(request))


def network(request):
	"""
	Page with network image
	"""
	# render page
	return render_to_response('network.html', context_instance=RequestContext(request))


def protein_detail(request, common_name):
	"""
	Page for each protein, with protein's videos, matrices, and other information
	"""
	# get protein from common name, its videos
	p = get_object_or_404(Protein, common_name=common_name)
	v = Video.objects.filter(protein_id=p.id)

	# get all compartments and timepoints
	c = Compartment.objects.all()
	t = Timepoint.objects.all()
	num_timepoints = len(t)

	matrices = [] # list of matrices. Each element: [video.id or "merge"][corresponding matrix]
	
	for video in v:
		# if summary length is longer than can fit on page
		if len(video.summary) > 600:
			# add truncated summary to video
			video.truncated_summary = video.summary[:500]
		
		# get the strain corresponding to the video, and process the strain's genotype
		video.strain = get_object_or_404(Strain, id=video.strain_id) # get strain
		
		# if Miyeko's strain, generate genotype from vector and protein.
		if video.strain.genotype == 'pJon': 
			video.strain.genotype = "unc-119(ed3) III; nnIs[unc-119(+) + Ppie-1::GFP-TEV-STag::" + p.common_name + "::3'pie-1]"
		elif video.strain.genotype == 'pDESTMB16':
			video.strain.genotype = "unc-119(ed3) III; nnIs[unc-119(+) + Ppie-1::" + p.common_name + "::GFP::3'pie-1]"
		
		# if non-Miyeko-made strains missing a hard-coded genotype entry in the database, it means they can be linked to on WormBase
		if not video.strain.genotype:
			video.strain.wormbase = "http://www.wormbase.org/species/c_elegans/strain/" + video.strain.name
		
		signals = SignalRaw.objects.filter(video_id=video.id) # get all signals as one list
		matrix = [] # list of rows for this matrix. Each element: [compartment][list of signals for that row]
		i = 0 # index for beginning of current row
		if signals:
			for compartment in c: # for each row
				matrix.append((compartment, signals[i:(i+num_timepoints)])) # add this row's compartment and signals
				i += num_timepoints
			matrices.append((video.id, matrix))
	
	# add the merge matrix to matrices
	matrix = [] # refresh matrix
	i = 0 # refresh index
	signals = SignalMerged.objects.filter(protein_id=p.id) # get all signals as one list
	if signals:
		for compartment in c: # for each row
			matrix.append((compartment, signals[i:(i+num_timepoints)])) # add this row's compartment and signals
			i += num_timepoints
		matrices.append(("merge", matrix))
	
	# render page
	return render_to_response('protein_detail.html', {
		'protein':p, 
		'videos':v,
		'timepoints':t,
		'matrices':matrices,
	}, context_instance=RequestContext(request))


def spatiotemporal_search(request):
	"""
	Page with spatiotemporal matrix showing number of proteins 
	expressed at every spatiotemporal point
	"""
	# get all compartments and timepoints
	c = Compartment.objects.all()
	t = Timepoint.objects.all()
	
	# create a 2D array of all 0s for the matrix signals	
	signal_matrix = [[0 for x in range(0, len(t)+1)] for x in range(0, len(c)+1)] 
	
	# get ALL merge signals
	signals = SignalMerged.objects.filter(Q(strength=2) | Q(strength=3))

	# iterate through signals, incrementing corresponding cell in matrix
	for signal in signals:
		signal_matrix[signal.compartment_id][signal.timepoint_id] += 1
	
	matrices = [] #2D array for matrices ["spatiotemporal"][corresponding matrix]
	matrix = [] # list of rows for this matrix. Each element: [compartment][list of signals for that row]

	for compartment in c:
		matrix.append((compartment, signal_matrix[compartment.id][1:]))

	matrices.append(("spatiotemporal", matrix))
	
	# render page
	return render_to_response('spatiotemporal_search.html', {
		'timepoints':t,
		'matrices':matrices,
	}, context_instance=RequestContext(request))


def spatiotemporal_both(request, compartment, timepoint):
	"""
	Results page for coexpressed proteins given a compartment AND timepoint
	"""
	# get this timepoint and compartment
	c = Compartment.objects.get(id=compartment)
	t = Timepoint.objects.get(id=timepoint)

	# get all proteins present or weak in this compartment at this timepoint
	s = SignalMerged.objects.filter(
		Q(compartment_id = compartment),
		Q(timepoint_id = timepoint),
		Q(strength=2) | Q(strength=3)
	)

	# render page
	return render_to_response('spatiotemporal_both.html', {
		'signals':s,
		'compartment':c,
		'timepoint':t
	}, context_instance=RequestContext(request))


def spatiotemporal_compartment(request, compartment):
	"""
	Results page for coexpressed proteins given a compartment only
	"""
	# get this compartment and ALL timepoints
	c = Compartment.objects.get(id=compartment)
	t = Timepoint.objects.all()
	
	# get all proteins present or weak at any time in this compartment 
	p = SignalMerged.objects.values('protein').filter(
		Q(compartment_id = compartment),
		Q(strength=2) | Q(strength=3)
	).distinct()

	# get ALL signals for these proteins in this compartments
	s = SignalMerged.objects.filter(
		Q(protein_id__in=p),
		Q(compartment_id = compartment)
	)

	# render page
	return render_to_response('spatiotemporal_compartment.html', {
		'signals':s,
		'compartment':c,
		'timepoints':t
	}, context_instance=RequestContext(request))

	
def spatiotemporal_timepoint(request, timepoint):
	"""
	Results page for coexpressed proteins given a timepoint only
	"""
	# get this timepoint and ALL compartments
	t = Timepoint.objects.get(id=timepoint)
	c = Compartment.objects.all()

	# get all proteins present or weak in any compartment at this timepoint
	p = SignalMerged.objects.values('protein').filter(
		Q(timepoint_id = timepoint), 
		Q(strength=2) | Q(strength=3)
	).distinct()

	# get ALL signals for these proteins at this timepoint
	s = SignalMerged.objects.filter(
		Q(protein__in=p),
		Q(timepoint_id = timepoint)
	)

	# render page
	return render_to_response('spatiotemporal_timepoint.html', {
		'signals':s,
		'timepoint':t,
		'compartments':c
	}, context_instance=RequestContext(request))
