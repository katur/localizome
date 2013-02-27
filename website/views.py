# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
#from django.views.generic import ListView
from django.template import RequestContext #extends Context; needed for STATIC_URL
from website.models import Protein
from website.models import Timepoint
from website.models import Compartment
import functions

# render_to_response() loads a template, passes it a context, and renders it
def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def protein_list(request):
	p = Protein.objects.all()
	return render_to_response('protein_list.html', {'proteins':p}, context_instance=RequestContext(request))

def protein_detail(request, common_name):
	p = get_object_or_404(Protein, common_name=common_name)
	c = Compartment.objects.all()
	t = Timepoint.objects.all()
	a = functions.create_matrix(c,t)
	#sig_merge = get_object_or_404(SignalMerge, protein_id = p.id)
	#sig_raw = get_object_or_404(SignalRaw, protein_id = p.id)
	return render_to_response('protein_detail.html', {'protein':p, 'compartments':c, 'timepoints':t}, context_instance=RequestContext(request))

def spaciotemporal(request):
	c = Compartment.objects.all()
	t = Timepoint.objects.all()
	return render_to_response('spaciotemporal.html', {'compartments':c, 'timepoints':t}, context_instance=RequestContext(request))

def network(request):
	return render_to_response('network.html', context_instance=RequestContext(request))

# below is to implement generic view ListView. I un-implemented it to simplify things.
# class ProteinList(ListView):
#	model = Protein
