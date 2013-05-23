from django.conf.urls import patterns, include, url

# urlpatterns is a module-level variable
urlpatterns = patterns('website.views', # first arg prefix for views
	# subsequent args are tuples: (regex, view, optional dictionary)
	url(
		r'^$',
		'home',
	),
	url(
		r'^proteins$',
		'protein_list',
	),
	url(
		r'^protein/(?P<common_name>.+)$',
		'protein_detail',
	),
	url(
		r'^spatiotemporal$',
		'spatiotemporal_search',
	),
	url(
		r'^spatiotemporal/compartment(?P<compartment>\d{1,2})/timepoint(?P<timepoint>\d{1,2})$',
		'spatiotemporal_both',
	),
	url(
		r'^spatiotemporal/compartment(?P<compartment>\d{1,2})$',
		'spatiotemporal_compartment',
	),
	url(
		r'^spatiotemporal/timepoint(?P<timepoint>\d{1,2})$',
		'spatiotemporal_timepoint',
	),
	url(
		r'^network$',
		'network',
	),
	url(
		r'^downloads$',
		'downloads',
	),
	url(
		r'^downloads/(?P<common_name>.+)$',
		'downloads_protein',
	),
)
