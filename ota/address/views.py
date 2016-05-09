from django.shortcuts import render
from django.http import HttpResponse
import json

from address.models import Country
from hotels.models import Hotel
from address.globals import *


# views below

def countries(request):
    countries = []
    results = []

    if request.is_ajax():
        countries = Country.objects.all()        

    for country in countries:
        results.append(country.country_name)
        code = country.country_code.lower()
        
        # fill up the global cc --> name cache and the reverse name --> cc
        if code not in cc_to_name:            
            cc_to_name[code] = country.country_name
            name_to_cc[country.country_name] = code

    print "global country cache added with", len(cc_to_name), "countries"

    jsonData = json.dumps(results)
    return HttpResponse(jsonData ,content_type="application/json")

def cities(request):
    city_list = []
    results = []

    city_hash = {}
    codes_nf = {}

    if request.is_ajax():        
        city_list = Hotel.objects.values('city', 'country_cc1').distinct()

    for c in city_list:
        code = c['country_cc1'].lower()        
        cityTrim = c['city'].strip()        
        if cityTrim != "":            
            if code not in cc_to_name:            
                codes_nf[code] = True                

                if cityTrim not in city_hash:
                    results.append( cityTrim )
                    city_hash[cityTrim] = True
            else:               
                
                if cityTrim not in city_hash:
                    results.append( cityTrim + ", " + cc_to_name[code] )
                    city_hash[cityTrim] = True            

    print "NF:", codes_nf
    
    jsonData = json.dumps(results)
    return HttpResponse(jsonData ,content_type="application/json")
        
    
    
