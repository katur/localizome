from django.conf.urls import patterns, include, url

# urlpatterns is a module-level variable
urlpatterns = patterns('website.views', # first arg prefix for views
	# subsequent args tuples: regex, view, optional dictionary
	url(r'^$', 'home', name='home_url'),
	url(r'^proteins$', 'protein_list', name='proteins_url'),
	url(r'^protein/(?P<common_name>.+)$', 'protein_detail', name='protein_detail_url'),
	url(r'^spaciotemporal$', 'spaciotemporal_search', name='spaciotemporal_search_url'),
	url(r'^spaciotemporal/compartment(?P<compartment>\d{1,2})/timepoint(?P<timepoint>\d{1,2})$', 'spaciotemporal_both', name='spaciotemporal_both_url'),
	url(r'^spaciotemporal/compartment(?P<compartment>\d{1,2})$', 'spaciotemporal_compartment', name='spaciotemporal_compartment_url'),
	url(r'^spaciotemporal/timepoint(?P<timepoint>\d{1,2})$', 'spaciotemporal_timepoint', name='spaciotemporal_timepoint_url'),
	url(r'^network$', 'network', name='network_url'),
)
