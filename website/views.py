from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes context, renders
from django.db.models import Q # enables AND and OR in SQL filters
from website.models import *
import numpy # enables deleting columns in 2D arrays

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
	# get protein from common name
	p = get_object_or_404(Protein, common_name=common_name)
	
	# get protein's videos and rep video
	v = Video.objects.filter(protein_id=p.id)
	rep_v = p.representative_video

	# get all compartments and timepoints
	c = Compartment.objects.all()
	t = Timepoint.objects.all()
	num_timepoints = len(t)

	# dictionaries to return compartment names and short names
	c_dict = {}
	for compartment in c:
		c_dict[compartment.id] = compartment.name
	c_dict_short = {}
	for compartment in c:
		c_dict_short[compartment.id] = compartment.short_name

	matrices = [] # 2D array for matrices: [video.id or "union"][matrix[] of signals]
	
	# add each video matrix to matrices[]
	for video in v:
		signals = SignalRaw.objects.filter(video_id=video.id) # get all 440 signals as one list
		matrix = [] # array of signals for one matrix (each array element is one row)
		i = 0 # index for beginning of current row
		for compartment in c: # for each row
			matrix.append((signals[i:(i+num_timepoints)])) # add next row to the matrix
			i += num_timepoints
		matrices.append((video.id, matrix)) # add matrix to matrices[]
	
	# add the union matrix to matrices[]
	matrix = [] # refresh matrix
	i = 0 # refresh index
	signals = SignalMerged.objects.filter(protein_id=p.id) # get all 440 signals as one list
	if signals:
		for compartment in c: # for each row
			matrix.append((signals[i:(i+num_timepoints)])) # add next row to the matrix
			i += num_timepoints
		matrices.append(("union", matrix)) # add union matrix to matrices[]
	
	# render page
	return render_to_response('protein_detail.html', {
		'protein':p, 
		'videos':v,
		'representative_video':rep_v,
		'timepoints':t,
		'compartment_dictionary':c_dict, 
		'compartment_dictionary_short':c_dict_short, 
		'matrices':matrices,
	}, context_instance=RequestContext(request))


def spatiotemporal_search(request):
	"""
	Page with spatiotemporal matrix showing number of proteins 
	expressed at every spatiotemporal point
	"""
	# get all compartments and timepoints, along with their quantities
	c = Compartment.objects.all()
	num_compartments = len(c)
	t = Timepoint.objects.all()
	num_timepoints = len(t)
	
	# dictionaries so that signals can be sorted by compartment_id more efficiently
	c_dict = {}
	for compartment in c:
		c_dict[compartment.id] = compartment.name
	c_dict_short = {}
	for compartment in c:
		c_dict_short[compartment.id] = compartment.short_name
	
	# NOTE: the below data structures for consistency with protein detail page
	matrices = [] #2D array for matrices ["spatiotemporal"][matrix[] of signals]
	
	# each element a row; init all cells to 0	
	matrix = [[0 for x in range(0, num_timepoints+1)] for x in range(0, num_compartments+1)] 
	
	# get ALL merged/unioned signals
	signals = SignalMerged.objects.filter(Q(strength=2) | Q(strength=3))

	# iterate through signals, incrementing corresponding matrix cells
	for signal in signals:
		matrix[signal.compartment_id][signal.timepoint_id] += 1
	
	# use numpy to cut out the 0th row and 0th column
	matrix = numpy.array(matrix)
	matrix = matrix[1:,1:]

	# add the resulting matrix to matrices[]
	matrices.append(("spatiotemporal", matrix))
	
	# render page
	return render_to_response('spatiotemporal_search.html', {
		'timepoints':t,
		'compartment_dictionary':c_dict,
		'compartment_dictionary_short':c_dict_short,
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
