from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from website.models import Protein

# urlpatterns is a module-level variable.
# it is a sequence of tuples, each in the format: 
# (regex, Python callback fxn [,optional dictionary])

urlpatterns = patterns('',
    url(r'^$', 'website.views.home', name='home'),
    url(r'^proteins$', 
	    ListView.as_view(
		    queryset = Protein.objects.order_by('common_name'),
		    context_object_name='protein_list',
		    template_name='protein_list.html')),
#    url(r'^protein/(?P<pk>.+)$', 
#	    DetailView.as_view(
#		    model=Protein,
#		    template_name='protein_detail.html')),
    url(r'^protein/(?P<protein_common_name>.+)$', 'website.views.protein_detail'),    
    #url(r'^localizome/', include('localizome.foo.urls')),
)
