from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from hotels import forms as hotelForms
from address.globals import *
from core.utils import *
from hotels.search import hotel_search
from hotels.requestManager import *
import json
import logging
import uuid


MAX_PAGES_PER_PAGE = 8

def search(request):
    """
        Search request from main page
    """

    #
    # non-binding
    #
    hotelSearchForm = hotelForms.HotelSearchForm()

    #
    # Error lists
    #
    destErrors = []
    interestsErrors = []
    dateErrors = []

    #
    # data sent back for passing info
    # to booking.com
    #
    checkin_date = ""
    checkout_date = ""
    no_rooms = 1
    req_adults = 1
    req_children = 0

    #
    # dummy start/rating list
    #
    dummy_star_rating = range(5)

    if request.method == 'GET':

        #
        # bind the data
        #
        hotelSearchForm = hotelForms.HotelSearchForm( request.GET )

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
            # Difference between CheckIn and CheckOut date
            #
            delta_time = checkOutDate - checkInDate
            if  delta_time.days < 0:
                dateErrors.append( "CheckOut date can't be before CheckIn date!" )

            #
            # stars search ( hotel class - at least )
            #
            stars = request.GET.get('stars')
            
            #
            # Get session_guid from request
            #
            session_guid = request.GET.get('session_guid')

            #
            # Generate saved query for pagination
            #
            saved_query = ""
            if wellness:
                saved_query += "wellness=on&"
            if romance:
                saved_query += "romance=on&"
            if shopping:
                saved_query += "shopping=on&"
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
                saved_query += "checkInDate=" + str(checkInDate) + "&"
                checkin_date = str(checkInDate)
            if checkOutDate:
                saved_query += "checkOutDate=" + str(checkOutDate) + "&"
                checkout_date = str(checkOutDate)
            if rooms:
                saved_query += "rooms=" + str(rooms) + "&"
                no_rooms = str(rooms)
            if adults:
                saved_query += "adults=" + str(adults) + "&"
                req_adults = str(adults)
            if children:
                saved_query += "children=" + str(children) + "&"
                req_children =  str(children)

            #
            # add Session GUID to saved query string (generate new one if None)
            #
            if session_guid == None:
                session_guid = uuid.uuid4()
                
            saved_query += "session_guid=" + str(session_guid) + "&"         
                           
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

            if len(dateErrors) != 0:
                
                 return render(request,
                      "index.html",
                      {'hotelSearchForm': hotelSearchForm,
                       'dateErrors': dateErrors})
            
            #
            # Search now
            #
            (hotels_list, query_dest_trimmed) = hotel_search( destination,
                                                              interest_dict,
                                                              surpriseme,
                                                              stars,
                                                              session_guid )
            
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

            #
            # initialize fields not specified in request
            #
            pageCurrent = None
            try:
                pageCurrent = int(page)
            except:
                pageCurrent = 1

            #
            # when no stars is specified (set to 0)
            #
            if stars == None:
                stars = 0                 
            
            return render(request,
                      "search_results.html",
                      {'hotels': hotels,
                       'hotelSearchForm': hotelSearchForm,
                       'destination': destination,
                       'interest_dict' : json.dumps(interest_dict),
                       'surpriseme': surpriseme,
                       'checkin': checkin_date,
                       'checkout': checkout_date,
                       'req_adults': req_adults,
                       'req_children': req_children,
                       'no_rooms': no_rooms,
                       'dummy_star_rating': dummy_star_rating,
                       'saved_query': saved_query,
                       'pageRange': pageRange,
                       'aid': BOOKING_AID,
                       'query_dest_trimmed': query_dest_trimmed,
                       'page': pageCurrent,
                       'stars': stars,
                       'session_guid': session_guid,
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
        # return error on Non-GET / Non-POST request
        #
        return None


def bookNow( request ):
    """
        Trigerred on Book Now click in main page
        Keeps track of these requests for statistical purposed.
        Receives AJAX request
    """

    if request.is_ajax():

        coorelation_id = request.POST.get('book_session_guid')
        hotel_id_str = request.POST.get('book_hotel_id')

        if hotel_id_str != None and coorelation_id != None:

            print type(hotel_id_str)
            print type(coorelation_id)

            #
            # convert hotel_id str to int
            #
            try:
                hotel_id = int( hotel_id_str )
                print "hotel_id", hotel_id
            except ValueError as ve:
                print "ValueError", ve

            #
            # convert UUID str to UUID
            #
            try:
                coorelation_id = uuid.UUID(coorelation_id)
                print "coorelation_id", coorelation_id
            except ValueError as ve:
                print "ValueError badly formed hexadecimal.", ve

            #
            # Enqueue bookNow requests for addition
            #
            QueueRequestsManager.EnqueueBookNowRequest( coorelation_id, hotel_id )            
           
        else:
            print "hotel ID or session GUID is NULL"
            print "hotel_id_str", hotel_id_str
            print "coorelation_id", coorelation_id
            

    else:
        print "The request is non-ajax. No operation was done."

    return HttpResponse(json.dumps([]) ,content_type="application/json")
    
    
           
