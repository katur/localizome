# Create your views here.
from website.models import Protein
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
#from django.template import RequestContext
# Note: render_to_response() is a shortcut to load a template, pass it a context,
# and render it. See https://docs.djangoproject.com/en/1.4/intro/tutorial03/

def home(request):
	return render_to_response('home.html')

def protein_detail(request, common_name):
	p = get_object_or_404(Protein, common_name=common_name)
	return render_to_response('protein_detail.html', {'protein': p})
