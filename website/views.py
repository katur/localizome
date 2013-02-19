# Create your views here.
from website.models import Protein
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
# Note: render_to_response() is a shortcut to load a template, pass it a context,
# and render it. See https://docs.djangoproject.com/en/1.4/intro/tutorial03/


def home(request):
	return render_to_response('home.html')

def display_proteins(request):
	protein_list = Protein.objects.all().order_by('common_name')
	return render_to_response('protein_list.html', {'protein_list': protein_list})

def protein_detail(request, protein_common_name):
	p = get_object_or_404(Protein, common_name=protein_common_name)
	return render_to_response('protein_detail.html', {'protein': p})
