# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
#from django.views.generic import ListView
from django.template import RequestContext #extends Context; needed for STATIC_URL
from django.db.models import Q
from website.models import *
import functions
import numpy

# render_to_response() loads a template, passes it a context, and renders it
def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))


def protein_list(request):
	p = Protein.objects.all()
	return render_to_response('protein_list.html', {'proteins':p}, context_instance=RequestContext(request))


def protein_detail(request, common_name):
	p = get_object_or_404(Protein, common_name=common_name)
	v = Video.objects.filter(protein_id=p.id)
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

	matrices = [] # 2D array for matrices: [video.id or "merge][matrix of signals]
	matrix = [] # 2D array of signals for one matrix
	
	# FIRST: add the merge matrix to matrices
	signals = SignalMerged.objects.filter(protein_id=p.id) # first get all 440 signals as one list
	i = 0 # index for signal at beginning of current row
	for compartment in c: # for each row
		matrix.append((signals[i:(i+num_timepoints)])) # add next row to the matrix
		i += num_timepoints
	matrices.append(("merge", matrix))
	
	# THEN: add each video matrix to matrices
	for video in v:
		signals = SignalRaw.objects.filter(video_id=video.id) # get all 440 signals as one list
		matrix = [] # refresh matrix
		i = 0 # refresh index
		for compartment in c: # for each row
			matrix.append((signals[i:(i+num_timepoints)])) # add next row to the matrix
			i += num_timepoints
		matrices.append((video.id, matrix))
	
	return render_to_response('protein_detail.html', {
		'protein':p, 
		'timepoints':t,
		'videos':v,
		'compartment_dictionary':c_dict, 
		'compartment_dictionary_short':c_dict_short, 
		'matrices':matrices
	}, context_instance=RequestContext(request))


def spaciotemporal(request):
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
	
	# for consistency with multiple matrices of protein detail page, make a 2D array for matrices
	matrices = []

	# this time initialize the matrix to all 0s
	matrix = [[0 for x in range(0, num_timepoints+1)] for x in range(0, num_compartments+1)]
	
	signals = SignalMerged.objects.filter(Q(strength=2) | Q(strength=3)) # get ALL signals

	# iterate through signals, incrementing corresponding matrix cells
	for signal in signals:
		matrix[signal.compartment_id][signal.timepoint_id] += 1
	
	# turn into numpy array to cut out the first row and first column
	matrix = numpy.array(matrix)
	matrix = matrix[1:,1:]

	# add the spaciotemporal matrix to the matrices tuple
	matrices.append(("spaciotemporal", matrix))
	
	#color_gradient = []
	#for i in range(1, 5):
	#	start_index = (i-1)*5+1
	#	color_gradient.append((i, start_index, start_index+4))
	#
	#for i in range(5,10):
	#	start_index = i*10-29
	#	color_gradient.append((i, start_index, start_index+9))
	#
	#color_gradient.append((10, 71, "+"))

	return render_to_response('spaciotemporal.html', {
		'timepoints':t,
		'compartment_dictionary':c_dict,
		'compartment_dictionary_short':c_dict_short,
		'matrices':matrices,
	}, context_instance=RequestContext(request))


def network(request):
	return render_to_response('network.html', context_instance=RequestContext(request))

# below is to implement generic view ListView. I un-implemented it to simplify things.
# class ProteinList(ListView):
#	model = Protein
