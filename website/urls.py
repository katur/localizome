from django.conf.urls import url

from . import views


# urlpatterns is a module-level variable
urlpatterns = [
    url(r'^$', views.home,
        name='home_url'),
    url(r'^proteins/$', views.protein_list,
        name='protein_list_url'),
    url(r'^protein/(?P<common_name>.+)$', views.protein_detail,
        name='protein_detail_url'),
    url(r'^spatiotemporal/$', views.spatiotemporal_search,
        name='spatiotemporal_search_url'),
    url((r'^spatiotemporal/compartment(?P<compartment>\d{1,2})/'
         'timepoint(?P<timepoint>\d{1,2})$'),
        views.spatiotemporal_both, name='spatiotemporatl_both_url'),
    url(r'^spatiotemporal/compartment(?P<compartment>\d{1,2})$',
        views.spatiotemporal_compartment,
        name='spatiotemporal_compartment_url',),
    url(r'^spatiotemporal/timepoint(?P<timepoint>\d{1,2})$',
        views.spatiotemporal_timepoint,
        name='spatiotemporat_timepoint_url'),
    url(r'^network/$', views.network,
        name='network_url'),
    url(r'^downloads/$', views.downloads,
        name='downloads_url'),
    url(r'^downloads/(?P<common_name>.+)$', views.downloads_protein,
        name='downloads_protein_url'),
]
