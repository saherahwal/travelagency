from django.shortcuts import render
from django.http import HttpResponse
import json
import threading

from address.models import Country
from hotels.models import Hotel
from address.globals import *

#
# views below
#

def countries(request):
    countries = []
    results = []

    global global_countries

    global global_lock
    global_lock.acquire(True)

    if request.is_ajax():
        if global_countries == []:
            countries = Country.objects.all()
        else:
            countries = global_countries

    for country in countries:
        results.append(country.country_name)
        code = country.country_code.lower()
        
        # fill up the global cc --> name cache and the reverse name --> cc
        if code not in cc_to_name:            
            cc_to_name[code] = country.country_name
            name_to_cc[country.country_name] = code

    print "global country cache added with", len(cc_to_name), "countries"

    jsonData = json.dumps(results)
    
    global_lock.release()

    return HttpResponse(jsonData ,content_type="application/json")

def cities(request):
    city_list = []
    results = []

    global_lock.acquire(True)

    city_hash = {}
    codes_nf = {}

    global global_destination_list

    #
    # Retrieve City,Country code list from DB only at server start
    # then cache it in global_destination_list
    #
    if len(global_destination_list) == 0:
        if request.is_ajax():
            #
            # NOTE/WARNING: iteration over city_list fails if we don't have (city,country_cc1) index in the DB
            #
            city_list = Hotel.objects.values('city', 'country_cc1').distinct()
    
        #
        # NOTE/WARNING: iteration fails if we don't have (city,country_cc1) index in the DB
        #
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
        global_destination_list = results

    else:
        #
        # Get results from global cache
        #
        if request.is_ajax():
            results = global_destination_list
    
    jsonData = json.dumps(results)
    global_lock.release()
    return HttpResponse(jsonData ,content_type="application/json")
        
    
    
