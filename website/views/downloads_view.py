from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes context, renders
from website.models import *

def downloads(request):
	"""
	Generic download page
	"""	
	# render page
	return render_to_response('downloads.html', context_instance=RequestContext(request))


def downloads_protein(request, common_name):
	"""
	Download page including downloads for a specific protein
	"""
	p = get_object_or_404(Protein, common_name=common_name)
	v = Video.objects.filter(protein_id=p.id)

	for video in v:
		video.avi = video.filename + ".avi"
		video.mp4 = video.filename + ".mp4"
		video.ogv = video.filename + ".ogv"

	# render page
	return render_to_response('downloads.html', {
		'protein':p,
		'videos':v,
	}, context_instance=RequestContext(request))
