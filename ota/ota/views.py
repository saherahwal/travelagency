from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from hotels import forms as hotelForms
from ota import forms as otaForms
from hotels.models import TopInterestLocation
from random import Random
from datetime import datetime, timedelta
from core.utils import *

USER_VALID_AUTHENTICATED = "User is valid, active and authenticated"
USER_VALID_ACCOUNT_DISABLED = "Password valid, but account disabled"
AUTHENTICATION_FAIL = "Neither username nor email authentication worked. Password and/or username invalid"

def homepage(request):

    #
    # non-binding Hotel Search Form
    #
    hotelSearchForm = hotelForms.HotelSearchForm()

    #
    # get top interest destination searches - random 12
    #
    topInterestLocs = getTopInterestHotels( 12 )

    (checkInDate, checkOutDate) = getCheckInCheckOut()
   
    return render(request,
                  "index.html",
                  {'hotelSearchForm': hotelSearchForm,
                   'topInterestsLocations': topInterestLocs,
                   'checkInDate': checkInDate,
                   'checkOutDate': checkOutDate})

def topinterests(request):

    #
    # Retreive ID from request
    #
    topinterest_id = request.GET.get('id')

    if topinterest_id == None:

        #
        # retrieve top interest locations
        #
        topRes_wellness = getTopInterestHotels( 4, True, [WELLNESS] )
        topRes_adventure = getTopInterestHotels( 4, True, [ADVENTURE] )
        topRes_skiing = getTopInterestHotels( 4, True, [SKIING] )
        topRes_beachAndSun = getTopInterestHotels( 4, True, [BEACH_AND_SUN] )
        topRes_shopping = getTopInterestHotels( 4, True, [SHOPPING] )
        topRes_family = getTopInterestHotels( 4, True, [FAMILY] )
        topRes_clubbing = getTopInterestHotels( 4, True, [CLUBBING] )
        topRes_casinos = getTopInterestHotels( 4, True, [CASINOS] )
        topRes_historyAndCulture = getTopInterestHotels( 4, True, [HISTORY_CULTURE] )
        topRes_romance = getTopInterestHotels( 4, True, [ROMANCE] )
    
        #
        # retreive check-in / check-out date
        #
        (checkInDate, checkOutDate) = getCheckInCheckOut()

        return render(request,
                      "top_interests.html",
                      {'topRes_wellness': topRes_wellness,
                       'topRes_adventure': topRes_adventure,
                       'topRes_skiing': topRes_skiing,
                       'topRes_beachAndSun': topRes_beachAndSun,
                       'topRes_shopping': topRes_shopping,
                       'topRes_family': topRes_family,
                       'topRes_clubbing': topRes_clubbing,
                       'topRes_casinos': topRes_casinos,
                       'topRes_historyAndCulture': topRes_historyAndCulture,
                       'topRes_romance': topRes_romance,
                       'checkInDate': checkInDate,
                       'checkOutDate': checkOutDate})

    else:

        #
        # We have an ID, retrieve that value only.
        #

        try:
            topintObj = TopInterestLocation.objects.get( id = topinterest_id )

            return render( request,
                          'top_interest_single.html',
                          {'topInterestSel' : topintObj })
        
        except ObjectDoesNotExist:

            #
            # TODO:
            # show 404 not found page
            #
            print "top_interest with id", topinterest_id, "doesn't exist"

        except Exception as e:

            #
            # TODO:
            # show 404 not found page
            #
            print "Exception thrown while get TopInterest Obj", e

def contact(request):

    #
    # non-binding Contact-Us Form
    #
    contactUsForm = otaForms.ContactUsForm()

    return render( request,
                  "contact.html",
                  {'contactUsForm': contactUsForm})

def send_email(request):
     
    #
    # bind the data
    #
    contactUsForm = otaForms.ContactUsForm( request.POST )

    #
    # check form validity
    #
    if contactUsForm.is_valid():
        name = contactUsForm.cleaned_data['name']
        email = contactUsForm.cleaned_data['email']
        message = contactUsForm.cleaned_data['message']

        #
        # TODO: send email logic implementation
        #

        return render(request,
                     "contact.html",
                     {'contactUsForm': contactUsForm})

    else:
        #
        # case where contact-us form is not valid
        #

        return render(request,
                      "contact.html",
                      {'contactUsForm': contactUsForm})

def blog(request):    
    return render( request , "blog.html", {})

def signin(request):

    if request.method == 'GET':

        #
        # Create un-bound empty form
        #
        loginForm = otaForms.LoginForm()

        return render( request,
                      "login.html",
                      { 'loginForm':loginForm })

    elif request.method == 'POST':

        #
        # init error list
        #
        loginErrors = []

        #
        # create form instance to process form data
        #
        loginForm = otaForms.LoginForm( request.POST )

        #
        # check whether form is valid
        #
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']

            #
            # authenticate using email or username
            #
            (user, msg) = otaAuthenticate(username, password)

            if user is not None:

                #
                # non-binding Hotel Search Form
                #
                hotelSearchForm = hotelForms.HotelSearchForm()

                #
                # get top interest destination searches - random 12
                #
                topInterestLocs = getTopInterestHotels( 12 )

                (checkInDate, checkOutDate) = getCheckInCheckOut()

                #
                # login the authenticated user
                #
                login(request, user)
   
                return render(request,
                              "index.html",
                              {'hotelSearchForm': hotelSearchForm,
                               'topInterestsLocations': topInterestLocs,
                               'checkInDate': checkInDate,
                               'checkOutDate': checkOutDate})
            else:
                loginErrors.append( msg )
                return render( request, "login.html", { 'loginForm': loginForm,
                                                        'loginErrors': loginErrors })
        else:
            return render( request, "login.html", { 'loginForm': loginForm,
                                                    'loginErrors': loginErrors })
    else:

        #
        # Create un-bound empty form
        #
        loginForm = otaForms.LoginForm()

        return render( request,
                      "login.html",
                      { 'loginForm':loginForm })

@login_required(login_url='/login/')
def signout(request):
    #
    # logout the user from session
    #
    logout(request)

    #
    # Create new unbound Login Form
    #
    loginForm = otaForms.LoginForm()
    
    return render( request,
                   "login.html",
                   { 'loginForm':loginForm })

#
# helper methods defined below
#

#
# authentication helper methods
#

def authenticate_username(username, password):
    return authenticate(username=username, password=password)

def authenticate_email(email, password):
    try:
        user = User.objects.get(email__iexact=email)
        if user.check_password(password):
            # need to call authenticate before login - django docs
            return authenticate(username=user.username, password=password)            
        return None
    except ObjectDoesNotExist:
        return None

def otaAuthenticate( username, password ):
    user = authenticate_username(username, password)
    user_email = authenticate_email(username, password)
    if user is not None:        
        if user.is_active:
            return (user, USER_VALID_AUTHENTICATED)
        else:
            return (None, USER_VALID_ACCOUNT_DISABLED)
    elif user_email is not None:
        if user_email.is_active:
            return (user_email, USER_VALID_AUTHENTICATED)
        else:
            return (None, USER_VALID_ACCOUNT_DISABLED)
    else:
        return (None, AUTHENTICATION_FAIL)

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
        
    #
    # format the dates in mm/dd/yyyy
    #
    strCheckIn = str(checkInDate.month) + "/" + str(checkInDate.day) + "/" + str(checkInDate.year)
    strCheckOut = str(checkOutDate.month) + "/" + str(checkOutDate.day) + "/" + str(checkOutDate.year)

    return (strCheckIn, strCheckOut)
    

def getTopInterestHotels( numToReturn,
                          considerInterestMap = False,
                          interest_list = [] ):
    """
        Returns a random list of top interest hotel/interst searches
        with maximum numToReturn elements
    """
    #
    # generate random seed
    #
    _rand = Random()
    now = datetime.now()
    _rand.seed( now.microsecond )
    
    if not considerInterestMap:
        
        #
        # retrieve all top destination locations
        #
    
        topIntResults = TopInterestLocation.objects.filter( public = True )

        #
        # Admin user gets all top interests
        #
        if request.user != None:
            if  request.user.is_superuser:
                topIntResults = TopInterestLocation.objects.all( )

    else:

        #
        # initialize lookup-dictionary for input interests
        #
        interest_dict = {}
        for elt in TRAVEL_INTERESTS:
            interest_dict[elt] = False;
        for elt in interest_list:
            interest_dict[elt] = True;

        topIntResults = TopInterestLocation.objects.filter( familyInterest = interest_dict[FAMILY],
                                                            adventureInterest = interest_dict[ADVENTURE],
                                                            beachSunInterest = interest_dict[BEACH_AND_SUN],
                                                            casinosInterest = interest_dict[CASINOS],
                                                            historyCultureInterest = interest_dict[HISTORY_CULTURE],
                                                            clubbingInterest = interest_dict[CLUBBING],
                                                            romanceInterest = interest_dict[ROMANCE],
                                                            shoppingInterest = interest_dict[SHOPPING],
                                                            skiingInterest = interest_dict[SKIING],
                                                            wellnessInterest = interest_dict[WELLNESS],
                                                            public = True
                                                            )

        #
        # Admin user gets all top interests 
        #
        if request.user != None:
            if  request.user.is_superuser:
                topIntResults = TopInterestLocation.objects.filter( familyInterest = interest_dict[FAMILY],
                                                                    adventureInterest = interest_dict[ADVENTURE],
                                                                    beachSunInterest = interest_dict[BEACH_AND_SUN],
                                                                    casinosInterest = interest_dict[CASINOS],
                                                                    historyCultureInterest = interest_dict[HISTORY_CULTURE],
                                                                    clubbingInterest = interest_dict[CLUBBING],
                                                                    romanceInterest = interest_dict[ROMANCE],
                                                                    shoppingInterest = interest_dict[SHOPPING],
                                                                    skiingInterest = interest_dict[SKIING],
                                                                    wellnessInterest = interest_dict[WELLNESS],
                                                                    )
    #
    # shuffle the result
    #
    
    shuffled_results = sorted( topIntResults, key=lambda f: _rand.random())

    return shuffled_results[: numToReturn]

    

