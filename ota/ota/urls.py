from django.conf.urls import include, url
from django.contrib import admin

# import views
from ota.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'ota.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', homepage),                      # home page
    url('^hotels/', include('hotels.urls')), # generic hotels page
    url('^blog/$', blog),                     # blog
    url('^activities$', activities),          # activities
    url('^results$', results),

    url('^address/', include('address.urls')),
   

    url(r'^admin/', include(admin.site.urls)),
     
]
