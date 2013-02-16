# Create your views here.
from django.template import Context, loader
from website.models import Protein
from django.http import HttpResponse

def home(request):
	return HttpResponse("Early Embryo Localizome")

def proteins(request):
	protein_list = Protein.objects.all().order_by('common_name')
	t = loader.get_template('website/proteins.html')
	c = Context({
		'protein_list': protein_list,
	})
	return HttpResponse(t.render(c))

def protein(request, protein_common_name):
	return HttpResponse("Page for Protein " + protein_common_name)
