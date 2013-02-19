from django.conf.urls import patterns, include, url

# Note: to make the website app portable, all urls are listed in website.
# This file is for the entire project's urls.
# Since the entire project is currently only the website, this simply 
# references the exact same urls as the app.

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('website.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
