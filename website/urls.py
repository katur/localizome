from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from website.models import Protein

# urlpatterns is a module-level variable.
# first argument is prefix for the views.
# next is a sequence of tuples, each in the format: 
# (regex, Python callback fxn / viewname [,optional dictionary])

urlpatterns = patterns('website.views',
	url(r'^$', 'home', name='home_url'),
	url(r'^protein/(?P<protein_common_name>.+)$', 'protein_detail', name='protein_detail_url'),
	url(r'^proteins$', 
		ListView.as_view(
			queryset = Protein.objects.order_by('common_name'),
			context_object_name='protein_list',
			template_name='protein_list.html'),
		name='proteins_url'),
#    url(r'^protein/(?P<pk>.+)$', 
#	    DetailView.as_view(
#		    model=Protein,
#		    template_name='protein_detail.html')),
)
