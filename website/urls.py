from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

# urlpatterns is a module-level variable
urlpatterns = patterns('', # first arg prefix for views
	# subsequent args are tuples: (regex, view, optional dictionary)
	(r'^admin/', include(admin.site.urls)),
	url(
		r'^$',
		'website.views.home',
	),
	url(
		r'^proteins/$',
		'website.views.protein_list',
	),
	url(
		r'^protein/(?P<common_name>.+)$',
		'website.views.protein_detail',
	),
	url(
		r'^spatiotemporal/$',
		'website.views.spatiotemporal_search',
	),
	url(
		r'^spatiotemporal/compartment(?P<compartment>\d{1,2})/timepoint(?P<timepoint>\d{1,2})$',
		'website.views.spatiotemporal_both',
	),
	url(
		r'^spatiotemporal/compartment(?P<compartment>\d{1,2})$',
		'website.views.spatiotemporal_compartment',
	),
	url(
		r'^spatiotemporal/timepoint(?P<timepoint>\d{1,2})$',
		'website.views.spatiotemporal_timepoint',
	),
	url(
		r'^network/$',
		'website.views.network',
	),
	url(
		r'^downloads/$',
		'website.views.downloads',
	),
	url(
		r'^downloads/(?P<common_name>.+)$',
		'website.views.downloads_protein',
	),
	url(
		r'^downloads/$',
		'website.views.downloads_protein',
	),
)
