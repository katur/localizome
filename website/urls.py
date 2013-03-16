from django.conf.urls import patterns, include, url

# urlpatterns is a module-level variable
urlpatterns = patterns('website.views', # first arg prefix for views
	# subsequent args are tuples: (regex, view, optional dictionary)
	url(r'^$', 'home', name='home_url'),
	url(r'^proteins$', 'protein_list', name='proteins_url'),
	url(r'^network$', 'network', name='network_url'),
	url(r'^protein/(?P<common_name>.+)$', 'protein_detail', name='protein_detail_url'),
	url(r'^spatiotemporal$', 'spatiotemporal_search', name='spatiotemporal_search_url'),
	url(
		r'^spatiotemporal/compartment(?P<compartment>\d{1,2})/timepoint(?P<timepoint>\d{1,2})$',
		'spatiotemporal_both',
		name='spatiotemporal_both_url'
	),
	url(
		r'^spatiotemporal/compartment(?P<compartment>\d{1,2})$',
		'spatiotemporal_compartment',
		name='spatiotemporal_compartment_url'
	),
	url(
		r'^spatiotemporal/timepoint(?P<timepoint>\d{1,2})$',
		'spatiotemporal_timepoint',
		name='spatiotemporal_timepoint_url'
	),
)
