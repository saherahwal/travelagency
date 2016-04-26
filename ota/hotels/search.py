import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hotels.models import *
from address.globals import *
from core.utils import *

MAX_SURPRISE_RES = 100

#
# column names for Scores
#
score_column_names = { WELLNESS: "wellnessScore",
                       SHOPPING: "shoppingScore",
                       ROMANCE : "romanceScore",
                       CLUBBING: "clubbingScore",
                       CASINOS : "casinosScore",
                       ADVENTURE : "adventureScore",
                       BEACH_AND_SUN: "beachSunScore",
                       FAMILY : "familyScore",
                       SKIING : "skiingScore",
                       HISTORY_CULTURE: "historyCultureScore" }


def hotel_search( query, interests_bitmap, surprise_me, stars ):
    """
        query: destination query
        interests_bitmap: map of interests chosen ( e.g {wellness: True, shopping: False , ...etc })
        surprise_me: boolean, if true, we choose location (ignore query)
        stars: at least that number of stars of hotel

        query can be one of the following: (need to parse)            
            1. Continent
            2. Country
            3. State, United States
            4. City (State), United States
            5. City, Country

        return tuple of querySet result and trimmed destination (query)
        In case of surprise me the trimeed query is the one chosen by algorithm
    """

    trimmed_query = None
    if surprise_me:
        #
        # if surpriseMe is true - ignore query and retrieve new one
        #
        trimmed_query = surpriseme_query( interests_bitmap ).strip()
    else:
        #
        # trim query from leading/trailing spaces
        #
        trimmed_query = query.strip()       
   

    # scores
    scoreResults = None
    
    #
    # check query status ( continent / country / city ... etc )
    #
    if trimmed_query in continents_to_id:

        #
        # Continent case ( e.g Search = "Europe" )
        #
        cont_id = continents_to_id[trimmed_query]
        scoreResults = Scores.objects.filter( hotel__continent_id=cont_id )

    elif trimmed_query in name_to_cc:

        #
        # Country case ( e.g Search = "Jordan" )
        #
        country_cc = name_to_cc[ trimmed_query ]
        scoreResults = Scores.objects.filter( hotel__country_cc1=country_cc )

    elif trimmed_query in us_states_set:

        #
        # State case in US
        #
        state = trimmed_query
        scoreResults = Scores.objects.filter( hotel__country_cc1='us',
                                              hotel__city__contains = '(' + state + ')' )
    else:

        #
        # The rest cases:
        # 1. City (State), United States
        # 2. City, Country
        # 3. State, United States
        #

        query_no_paren = None
        par_min = None
        
        #
        # if paranthesis exists, remove that portion
        #
        if trimmed_query.find("(") != -1:
            par_min = trimmed_query[trimmed_query.find("("):trimmed_query.find(")")+1]
            query_no_paren = trimmed_query.replace( par_min, "")

        parse_comma_trim = None

        if query_no_paren != None:

            #
            # split comma and trip on non-parenthesized input
            #
            parse_comma_trim = [ e.strip() for e in query_no_paren.split(",")]
        else:
            
            #
            # split comma and trim
            #
            parse_comma_trim = [ e.strip() for e in trimmed_query.split(",")]            

        
        if len(parse_comma_trim) == 1:

            #
            # For this case: just search for city only
            #
            scoreResults = Scores.objects.filter( hotel__city__contains = parse_comma_trim[0] )
             
        else:
            
            #
            # hoping the length is 2 [ city, country ]
            #            
            first_term = parse_comma_trim[0]
            last_term = parse_comma_trim[-1]

            #
            # check if second term is country
            #
            if last_term in name_to_cc:
                country_cc = name_to_cc[last_term]

                if par_min == None:
                    scoreResults = Scores.objects.filter( hotel__country_cc1=country_cc,
                                                          hotel__city__contains = first_term )
                else:
                    scoreResults = Scores.objects.filter( hotel__country_cc1=country_cc,
                                                          hotel__city__contains = par_min,
                                                          hotel__city_preferred__contains = first_term )                                                           
            else:

                print "could not find", last_term, "in countries"

                if par_min == None:

                    #
                    # For this case: just search for city only
                    #
                    scoreResults = Scores.objects.filter( hotel__city__contains = first_term )
                else:

                    #
                    # Search with paranthesis inclusion and city term
                    #
                    scoreResults = Scores.objects.filter( hotel__city__contains = first_term,
                                                          hotel__city_preferred__contains = par_min )

    #
    # extra total column for score ordering ( order by DESC )
    #
    total_str = construct_totalscore_columns( interests_bitmap )
    finalRes = scoreResults.extra( select = { 'total': total_str }, order_by=('-total',))

    # filter stars if not None
    if stars != None:
        finalRes = finalRes.filter( hotel__hotel_class__gte = stars )

    return (finalRes, trimmed_query)

#
# Helper functions
#
def construct_totalscore_columns( interests_map ):
    """
        Given interest_map ( interest:True ), return string for total score based on database columns for SQL query
        e.g for interests picked (shopping, family), return "shoppingScore + familyScore" 
    """
    s_total = ""
    for elt in interests_map.keys():

        if interests_map[elt] == True:
            #
            # first column set
            #
            if s_total == "":
                s_total = score_column_names[elt]
            else:
                s_total = s_total + " + " +  score_column_names[elt]

    print "s_total", s_total
    return s_total

def surpriseme_query( interests_map ):
    """
        Return query for surprise me feature given interests_map
    """

    #
    # extra total column for score ordering ( order by DESC )
    #
    total_str = construct_totalscore_columns( interests_map )
    result = Scores.objects.extra( select = { 'total': total_str }, order_by=('-total',))[:MAX_SURPRISE_RES]

    random_res_picked = random.choice( result )

    cc = random_res_picked.hotel.country_cc1

    return cc_to_name[cc]
    
    
##    bool_list = [ True, False ]
##
##    pick_cont = random.choice( bool_list )
##
##    #
##    # Pick Continent randomly
##    #
##    if pick_cont:
##        cont = random.choice( continents_to_id.keys() )
##        return cont
##    else:
##
##        pick_country_state = random.choice( bool_list )
##
##        #
##        # pick random country or state
##        #
##        if pick_country_state:
##            country = random.choice( name_to_cc.keys() )
##            return country
##
##        else:
##            state = random.choice( us_states )
##            return state
    
