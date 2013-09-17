from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes context, renders
from website.models import *

def protein_list(request):
	"""
	Page listing all proteins tested
	"""
	# get all proteins
	p = Protein.objects.all().exclude(common_name="no GFP")
	c = get_object_or_404(Protein, common_name="no GFP")

	# render page
	return render_to_response('protein_list.html', {
		'proteins':p,
		'control':c
	}, context_instance=RequestContext(request))
