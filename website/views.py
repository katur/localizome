# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
#from django.views.generic import ListView
from django.template import RequestContext #extends Context; needed for STATIC_URL
from website.models import *
import functions

# render_to_response() loads a template, passes it a context, and renders it
def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def protein_list(request):
	p = Protein.objects.all()
	return render_to_response('protein_list.html', {'proteins':p}, context_instance=RequestContext(request))

def protein_detail(request, common_name):
	p = get_object_or_404(Protein, common_name=common_name)
	v = Video.objects.filter(protein_id=p.id)
	t = Timepoint.objects.all()
	c = Compartment.objects.all()

	# dictionaries so that signals can be sorted by compartment_id more efficiently
	c_dict = {}
	c_dict_short = {}
	for compartment in c:
		c_dict[compartment.id] = compartment.name
	for compartment in c:
		c_dict_short[compartment.id] = compartment.short_name

	# tuple	for signals. key: the video or the string "merge". value: list of the 440 signals.
	signals_tuple = []
	
	# add the merge matrix to the tuple
	signals_tuple.append(("merge", SignalMerged.objects.filter(protein_id=p.id), "merge"))
	
	# add the video matrices to the tuple
	for video in v:
		signals_tuple.append((video.id, SignalRaw.objects.filter(video_id=video.id))) # could also send notes in this tuple if need be
	
	return render_to_response('protein_detail.html', {
		'protein':p, 
		'timepoints':t, 
		'compartment_dictionary':c_dict, 
		'compartment_dictionary_short':c_dict_short, 
		'videos':v, 
		'signals_tuple':signals_tuple
	}, context_instance=RequestContext(request))

def spaciotemporal(request):
	c = Compartment.objects.all()
	t = Timepoint.objects.all()
	return render_to_response('spaciotemporal.html', {'compartments':c, 'timepoints':t}, context_instance=RequestContext(request))

def network(request):
	return render_to_response('network.html', context_instance=RequestContext(request))

# below is to implement generic view ListView. I un-implemented it to simplify things.
# class ProteinList(ListView):
#	model = Protein
