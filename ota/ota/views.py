from django.shortcuts import render
from hotels import forms as hotelForms
from hotels.models import TopInterestLocation
from random import Random
from datetime import datetime, timedelta

def homepage(request):

    #
    # non-binding Hotel Search Form
    #
    hotelSearchForm = hotelForms.HotelSearchForm()

    #
    # get top interest destination searches - random 4
    #
    topInterestLocs = getTopInterestHotels( 4 )

    (checkInDate, checkOutDate) = getCheckInCheckOut()
   
    return render(request,
                  "index.html",
                  {'hotelSearchForm': hotelSearchForm,
                   'topInterestsLocations': topInterestLocs,
                   'checkInDate': checkInDate,
                   'checkOutDate': checkOutDate})

def hotels(request):    
    return render( request , "hotels.html", {})

def blog(request):    
    return render( request , "blog.html", {})

def activities(request):    
    return render( request , "activities.html", {})

def results(request):    
    return render( request , "results.html", {})


#
# helper methods defined below
#

def getCheckInCheckOut():
    """
        Return check-in / check-out date pairs
        since they are required by search.
        We choose next weekend by default
    """

    today = datetime.today()

    #
    # days to add to day for check-in
    #
    days_to_add = 0

    #
    # weekday (0 -> 6) (Monday -> Sunday)
    #
    weekday = today.weekday()

    #
    # pick weekend within 1-2 weeks
    #
    days_to_add = 7 + ( 5 - weekday )

    #
    # check-in / check-out
    #
    checkInDate = today + timedelta( days = days_to_add )
    checkOutDate = checkInDate + timedelta( days = 3 )

    checkInDate = checkInDate.date()
    checkOutDate = checkOutDate.date()    
        
    print "check-in", checkInDate
    print "check-out", checkOutDate

    strCheckIn = str(checkInDate.month) + "/" + str(checkInDate.day) + "/" + str(checkInDate.year)
    strCheckOut = str(checkOutDate.month) + "/" + str(checkOutDate.day) + "/" + str(checkOutDate.year)

    return (strCheckIn, strCheckOut)
    

def getTopInterestHotels( numToReturn ):
    """
        Returns a random list of top interest hotel/interst searches
        with maximum numToReturn elements
    """

    _rand = Random()
    now = datetime.now()
    _rand.seed( now.microsecond )
    
    #
    # retrieve all top destination locations
    #
    
    allTopLocations = TopInterestLocation.objects.all()

    #
    # shuffle the result
    #
    
    shuffled_results = sorted( allTopLocations, key=lambda f: _rand.random())

    return shuffled_results[: numToReturn]

    

