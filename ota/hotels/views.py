from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hotels import forms as hotelForms
from address.globals import *
from core.utils import *
from hotels.search import hotel_search
import json
import logging

MAX_PAGES_PER_PAGE = 8

def search(request):

    #
    # non-binding
    #
    hotelSearchForm = hotelForms.HotelSearchForm()

    #
    # Error lists
    #
    destErrors = []
    interestsErrors = []

    #
    # dummy start/rating list
    #
    dummy_star_rating = range(5)

    if request.method == 'GET':

        #
        # bind the data
        #
        hotelSearchForm = hotelForms.HotelSearchForm( request.GET )

##        _destination = request.GET.get('saved_destination')
##
##        if _destination != None:           
##
##            #
##            # This case where we paginate after the search
##            #
##
##            _destination = request.GET.get('saved_destination')
##            _interestmap = request.GET.get('saved_interestmap')
##            _surpriseme = request.GET.get('saved_surpriseme')
##
##            interest_dict = json.load( _interestmap )
##
##            destination = _destination
##            surpriseme = False
##            if _surpriseme == "True":
##                surpriseme = True
##
##            #
##            # Search now
##            #
##            hotels_list = hotel_search( destination, interest_dict, surpriseme )
##            paginator = Paginator(hotels_list, 18) # Show 18 hotels per page
##
##            page = request.GET.get('page')
##
##            try:
##                hotels = paginator.page(page)
##            except PageNotAnInteger:
##                # If page is not an integer, deliver first page.
##                hotels = paginator.page(1)
##            except EmptyPage:
##                # If page is out of range, deliver last page of results.
##                hotels = paginator.page(paginator.num_pages)
##
##            return render(request,
##                      "search_results.html",
##                      {'hotels': hotels,
##                       'hotelSearchForm': hotelSearchForm,
##                       'destination': destination,
##                       'interest_dict' : json.dumps(interest_dict),
##                       'surpriseme': surpriseme,
##                       'dummy_star_rating': dummy_star_rating})                

        #
        # check form validity of Form (this is the initial search
        #
        if hotelSearchForm.is_valid():
            wellness = hotelSearchForm.cleaned_data['wellness']
            romance = hotelSearchForm.cleaned_data['romance']
            casinos = hotelSearchForm.cleaned_data['casinos']
            beachAndSun = hotelSearchForm.cleaned_data['beachAndSun']
            skiing = hotelSearchForm.cleaned_data['skiing']
            shopping = hotelSearchForm.cleaned_data['shopping']
            nightlife = hotelSearchForm.cleaned_data['nightlife']
            adventure = hotelSearchForm.cleaned_data['adventure']
            family = hotelSearchForm.cleaned_data['family']
            historyAndCulture = hotelSearchForm.cleaned_data['historyAndCulture']            
           
            destination = hotelSearchForm.cleaned_data['destination']
            surpriseme = hotelSearchForm.cleaned_data['surpriseme']
            
            checkInDate = hotelSearchForm.cleaned_data['checkInDate']
            checkOutDate = hotelSearchForm.cleaned_data['checkOutDate']

            rooms = hotelSearchForm.cleaned_data['rooms']
            adults = hotelSearchForm.cleaned_data['adults']
            children = hotelSearchForm.cleaned_data['children']

            #
            # Generate saved query for pagination
            #
            saved_query = ""
            if wellness:
                saved_query += "wellness=on&"
            if romance:
                saved_query += "romance=on&"
            if wellness:
                saved_query += "wellness=on&"
            if casinos:
                saved_query += "casinos=on&"
            if beachAndSun:
                saved_query += "beachAndSun=on&"
            if skiing:
                saved_query += "skiing=on&"
            if nightlife:
                saved_query += "nightlife=on&"
            if adventure:
                saved_query += "adventure=on&"
            if family:
                saved_query += "family=on&"
            if historyAndCulture:
                saved_query += "historyAndCulture=on&"
            if surpriseme:
                saved_query += "surpriseme=on&"
            if checkInDate:
                saved_query += "checkInDate=" + checkInDate + "&"
            if checkOutDate:
                saved_query += "checkOutDate=" + checkOutDate + "&"
            if rooms:
                saved_query += "rooms=" + rooms + "&"
            if adults:
                saved_query += "adults=" + adults + "&"
            if children:
                saved_query += "children=" + children + "&"           

            saved_query = saved_query[:-1] # remove trailing &            

            #
            # init interests dictionary
            #
            interest_dict = { WELLNESS: wellness,
                              SHOPPING: shopping,
                              ROMANCE : romance,
                              CLUBBING: nightlife,
                              CASINOS : casinos,
                              ADVENTURE : adventure,
                              BEACH_AND_SUN: beachAndSun,
                              FAMILY : family,
                              SKIING : skiing,
                              HISTORY_CULTURE: historyAndCulture }

            #
            # We require destination input when SurpriseMe checkbox is un-checked.
            #
            if (surpriseme == False and destination == "" ):
                destErrors.append( "Field required when Surprise Me unchecked." )

            #
            # At least one interest should be checked
            #            
            anyInterestChecked = False
            for k,v in interest_dict.iteritems():
                # once we find a checked interest - break
                if v :
                    anyInterestChecked = True
                    break

            if not anyInterestChecked:
                interestsErrors.append( "Please check at least one interest." )
            

            if len(destErrors) != 0:

                return render(request,
                      "index.html",
                      {'hotelSearchForm': hotelSearchForm,
                       'destErrors': destErrors})

            if len(interestsErrors) != 0:

                return render(request,
                      "index.html",
                      {'hotelSearchForm': hotelSearchForm,
                       'interestsErrors': interestsErrors})
            
            #
            # Search now
            #
            (hotels_list, query_dest_trimmed) = hotel_search( destination, interest_dict, surpriseme )
            paginator = Paginator(hotels_list, 18) # Show 18 hotels per page

            page = request.GET.get('page')
           
            try:
                hotels = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                hotels = paginator.page(1)
            except EmptyPage:
                # If page is out of range, deliver last page of results.
                hotels = paginator.page(paginator.num_pages)


            print "hotels.paginator.num_pages", hotels.paginator.num_pages

            #
            # set page ranges for rendering pagination links
            #
            if page:

                if int(page) + MAX_PAGES_PER_PAGE <= hotels.paginator.num_pages:                    
                    endPage = int(page) + MAX_PAGES_PER_PAGE
                    pageRange = range( int(page), endPage)
                    print "endPage", endPage
                    print pageRange
                else:
                    startPage = max(hotels.paginator.num_pages - MAX_PAGES_PER_PAGE, 1)
                    pageRange = range(startPage, hotels.paginator.num_pages )
                    print "startPage", startPage
                    print pageRange
                                
            else:
                endPage = min( hotels.paginator.num_pages, MAX_PAGES_PER_PAGE )
                pageRange = range(1, endPage)
            
            return render(request,
                      "search_results.html",
                      {'hotels': hotels,
                       'hotelSearchForm': hotelSearchForm,
                       'destination': destination,
                       'interest_dict' : json.dumps(interest_dict),
                       'surpriseme': surpriseme,
                       'dummy_star_rating': dummy_star_rating,
                       'saved_query': saved_query,
                       'pageRange': pageRange,
                       'aid': BOOKING_AID,
                       'query_dest_trimmed': query_dest_trimmed,
                       WELLNESS: wellness,
                       SHOPPING: shopping,
                       ROMANCE : romance,
                       CLUBBING: nightlife,
                       CASINOS : casinos,
                       ADVENTURE : adventure,
                       BEACH_AND_SUN: beachAndSun,
                       FAMILY : family,
                       SKIING : skiing,
                       HISTORY_CULTURE: historyAndCulture })

        else:
            #
            # case where hotel search form is not valid
            #
                                    
            return render(request,
                      "index.html",
                      {'hotelSearchForm': hotelSearchForm})            
   
    else:
        
        #
        # return error on Non-GET/ Non-POST request
        #
        return None
           
