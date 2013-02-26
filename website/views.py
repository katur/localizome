# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
#from django.views.generic import ListView
from django.template import RequestContext #extends Context; needed for STATIC_URL
from website.models import Protein
from website.models import Timepoint
from website.models import Compartment

# render_to_response() loads a template, passes it a context, and renders it
def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def protein_list(request):
	p = Protein.objects.all()
	return render_to_response('protein_list.html', {'proteins': p}, context_instance=RequestContext(request))

def protein_detail(request, common_name):
	p = get_object_or_404(Protein, common_name=common_name)
	c = Compartment.objects.all()
	t = Timepoint.objects.all()
	return render_to_response('protein_detail.html', {'protein': p, 'compartments': c, 'timepoints' : t}, context_instance=RequestContext(request))

def spaciotemporal(request):
	return render_to_response('spaciotemporal.html', context_instance=RequestContext(request))

def contact(request):
	return render_to_response('contact.html', context_instance=RequestContext(request))

# below is to implement generic view ListView. I un-implemented it to simplify things.
# class ProteinList(ListView):
#	model = Protein
