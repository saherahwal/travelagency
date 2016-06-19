from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# import views
from ota.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'ota.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', homepage),                      # home page
    url('^hotels/', include('hotels.urls')), # generic hotels page

    url('^address/', include('address.urls')),
    url('^blog/', include('blog.urls')),                     # blog

    url('^topinterests/', topinterests),           # topinterests
    url('^contact/$', contact),                     # contact
    url('^contact/send_email/$', send_email),                     # contact

    url('^login/$', signin ), # login
    url('^logout/$', signout ), # logout
  
    url(r'^admin/', include(admin.site.urls)),
     
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
