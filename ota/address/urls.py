from django.conf.urls import include, url
from django.contrib import admin

#import views
from address.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'ota.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

  
    url('^allcountries/$', countries),
    url('^allcities/$', cities),

     
]
