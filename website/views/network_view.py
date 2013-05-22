from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes context, renders
from website.models import *

def network(request):
	"""
	Page with network image
	"""
	p = Protein.objects.filter(network_x_coordinate__isnull=False)

	for protein in p:
		protein.network_x_coordinate_adjusted = protein.network_x_coordinate - 30
		protein.network_y_coordinate_adjusted	= protein.network_y_coordinate - 5

	# render page
	return render_to_response('network.html', {
		'proteins':p,
	}, context_instance=RequestContext(request))
