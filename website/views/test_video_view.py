from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes context, renders

def test_video(request):
	# render page
	return render_to_response('test_video.html', context_instance=RequestContext(request))
