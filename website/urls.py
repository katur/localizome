from django.conf.urls import patterns, include, url
from website.views import ProteinList

# urlpatterns is a module-level variable
urlpatterns = patterns('website.views', # first arg prefix for views
	# subsequent args tuples: regex, view, optional dictionary
	url(r'^$', 'home', name='home_url'),
	url(r'^proteins$', ProteinList.as_view(template_name='protein_list.html'), 
		name='proteins_url'),
	url(r'^protein/(?P<common_name>.+)$', 'protein_detail', 
		name='protein_detail_url')
	#    url(r'^protein/(?P<pk>.+)$', 
#	    DetailView.as_view( # a generic disply view
#		    model=Protein,
#		    template_name='protein_detail.html')),
)