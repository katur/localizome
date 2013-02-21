# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView
from django.template import RequestContext #extends Context; needed for STATIC_URL
from website.models import Protein

# render_to_response() loads a template, passes it a context, and renders it
def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

class ProteinList(ListView):
	model = Protein

def protein_detail(request, common_name):
	p = get_object_or_404(Protein, common_name=common_name)
	return render_to_response('protein_detail.html', {'protein': p}, context_instance=RequestContext(request))
