from django.conf.urls import patterns, include, url

# urlpatterns is a module-level variable.
# it is a sequence of tuples, each in the format: 
# (regex, Python callback fxn [,optional dictionary])

urlpatterns = patterns('website.views',
    url(r'^$', 'home', name='home'),
    url(r'^proteins$', 'display_proteins', name='proteins'),
    url(r'^protein/(?P<protein_common_name>.+)$', 'protein_detail'),
    #url(r'^localizome/', include('localizome.foo.urls')),
)
