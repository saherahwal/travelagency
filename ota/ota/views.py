from django.shortcuts import render
from hotels import forms as hotelForms

def homepage(request):

    #
    # non-binding Hotel Search Form
    #
    hotelSearchForm = hotelForms.HotelSearchForm()
   
    return render(request,
                  "index.html",
                  {'hotelSearchForm': hotelSearchForm })

def hotels(request):    
    return render( request , "hotels.html", {})

def blog(request):    
    return render( request , "blog.html", {})

def activities(request):    
    return render( request , "activities.html", {})

def results(request):    
    return render( request , "results.html", {})
