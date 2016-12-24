import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hotels.models import *
from address.globals import *
from core.utils import *
from hotels.requestManager import *
from hotels.destinationManager import *
from core.marker import MIN_SCORE

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

#
# Create global Queue manager
#
queueMgr = QueueRequestsManager()
print "Created the queue manager"

def hotel_search( destinationObj, interests_bitmap, surprise_me, stars, session_guid):

    continent_id = None
    country_code = None
    city = None
    results = None
    interest_map = interests_bitmap

    #
    # Initialize and construct the extra column and where clause for total score search
    # minimum score depends on interests chosen.
    #
    (total_str, interest_count, s_where_clause) = construct_totalscore_columns( interests_bitmap )
    minimum_score = MIN_SCORE * interest_count

    if not surprise_me:

        #
        # Retrieve main destination attributes
        #
        city = destinationObj.getCity()
        state = destinationObj.getState()
        country_code = destinationObj.getCountryCode()

        #
        # Continent query
        #
        trimmed_continent_name = destinationObj.getContinent().strip()
        if trimmed_continent_name in continents_to_id:
            #
            # Continent case ( e.g Search = "Europe" )
            #
            continent_id = continents_to_id[trimmed_continent_name]
            results = Score.objects.filter( hotel__continent_id=continent_id )

        #
        # All other queries:
        #   1  City, State, Country
        #   2. City, Country
        #   3. State, Country 
        #   4. City, State
        #   5. Country
        #   6. City
        #   7. State
        #

        if city != "" and country_code != "" and state !="":

            #
            # Search (State) in US or Canada
            #
            if country_code.lower() == 'ca' or country_code.lower() == 'us':
                print "Search (State) in US or Canada"
                results =  Score.objects.filter( hotel__country_cc1=country_code,
                                                 hotel__city_preferred=city,
                                                 hotel__city__contains= '(' + state + ')' )

                #
                # If no results --> try city and country only
                #
                if results.count() == 0:
                    destinationObj.clearState()
                    results =  Score.objects.filter( hotel__country_cc1=country_code,
                                                     hotel__city_preferred=city )
            else:
                #
                # Other countries ( disregard state )
                #
                print "Other countries ( disregard state )"
                results =  Score.objects.filter( hotel__country_cc1=country_code,
                                                 hotel__city_preferred=city )

                #
                # If no results --> try the other city column
                #
                if results.count() == 0:
                    results =  Score.objects.filter( hotel__country_cc1=country_code,
                                                     hotel__city__contains=city )
        
        elif city != "" and country_code != "":
            print "city, country input only"
            results =  Score.objects.filter( hotel__country_cc1=country_code,
                                             hotel__city_preferred=city )

            #
            # If no results --> try the other city column
            #
            if results.count() == 0:
                results =  Score.objects.filter( hotel__country_cc1=country_code,
                                                 hotel__city__contains=city )
        elif state != "" and country_code != "":
            print "state, country input only"
            results =  Score.objects.filter( hotel__country_cc1=country_code,
                                             hotel__city__contains= '(' + state + ')' )

            #
            # If no results --> try to broaden to country
            #
            if results.count() == 0:
                destinationObj.clearState()
                results = Score.objects.filter( hotel__country_cc1=country_code  )

        elif state != "" and city != "":
            print "state, city input only"
            results =  Score.objects.filter( hotel__city__contains =  city + ' (' + state + ')' )

            #
            # If no results --> try state only
            #
            if results.count() == 0:
                destinationObj.clearCity()
                results =  Score.objects.filter( hotel__city__contains =  state )

        elif country_code != "":
            print "lonely country input only"
            results = Score.objects.filter( hotel__country_cc1=country_code )

        elif city != "":
            print "lonely city input only"
            results =  Score.objects.filter( hotel__city_preferred=city )

        elif state != "":
            print "lonely state input only"
            results =  Score.objects.filter(  hotel__city__contains= '(' + state + ')' )

            #
            # If no results --> try w/o parenths
            #
            if results.count() == 0:
                results =  Score.objects.filter( hotel__city__contains = state )

    else:
        #
        # SurpriseMe case
        #
        print "s_where_clause:", s_where_clause

        #
        # 1. Get MAX_SURPRISE_RES results
        # 2. pick a random country
        # 3. overwrite country code and DestinationObj
        # 4. search again
        #
        results = Score.objects.extra( select = { 'total': total_str },  where = [s_where_clause], params = [MIN_SCORE] * interest_count, order_by=('-total',))[:MAX_SURPRISE_RES]
        
        random_res_picked = random.choice( results )

        country_code = random_res_picked.hotel.country_cc1
        destinationObj = DestinationObj( "", country_code, "", "")

        results = Score.objects.filter( hotel__country_cc1=country_code )

    #
    # TODO: Ensure results is not None
    #

    #
    # Add extra column total for summation of relevant scores, order by descending
    # where clause: ( scoreA > min or ScoreB > min ...) to be more inclusive of results
    #    
    if (interest_count > 0):
        print "s_where_clause:", s_where_clause
        finalResult = results.extra( select = { 'total': total_str },  where = [s_where_clause], params = [MIN_SCORE] * interest_count, order_by=('-total',))
    else:
        print "no interests chosen"
        finalResult = results

    #
    # filter stars if not None
    # TODO: invetigate performance optimization of including in original queries above
    #
    if stars != None:
        finalResult = finalResult.filter( hotel__hotel_class__gte = stars )

    #
    # Enqueue search requests
    #
    QueueRequestsManager.EnqueueSearchRequest( session_guid, continent_id, country_code, city, interest_map, surprise_me )

    return (finalResult, destinationObj)


def hotel_search_deprecated( query, interests_bitmap, surprise_me, stars, session_guid ):
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

    #
    # define/init all needed variables
    # for Enqueuing requests for writes
    #
    cont_id = None
    country_code = None
    city = None
    interest_map = interests_bitmap
    surpriseme = surprise_me

    # scores
    scoreResults = filter_scoreresults_no_min( interest_map )

    #
    # Trim the query before figuring out its' category (city, continent, country...etc)
    #
    trimmed_query = None
    if surprise_me:
        #
        # if surpriseMe is true - ignore query and retrieve new one
        #
        (trimmed_query, scoreResults) = surpriseme_query( interests_bitmap, scoreResults )
        trimmed_query = trimmed_query.strip()
    else:
        #
        # trim query from leading/trailing spaces
        #
        trimmed_query = query.strip()
    
    #
    # check query status ( continent / country / city ... etc )
    #
    if trimmed_query in continents_to_id:
        
        #
        # Continent case ( e.g Search = "Europe" )
        #
        cont_id = continents_to_id[trimmed_query]
        scoreResults = scoreResults.filter( hotel__continent_id=cont_id )

    elif trimmed_query in name_to_cc:
        
        #
        # Country case ( e.g Search = "Jordan" )
        #
        country_cc = name_to_cc[ trimmed_query ]
        scoreResults = scoreResults.filter( hotel__country_cc1=country_cc )
        country_code = country_cc
        
    elif trimmed_query in us_states_set:

        #
        # State case in US
        #
        state = trimmed_query
        scoreResults = scoreResults.filter( hotel__country_cc1='us',
                                            hotel__city__contains = '(' + state + ')' )

        #
        # for now, use city field for state in request queue
        #
        city = state
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
            # split comma and strip on non-parenthesized input
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
            scoreResults = scoreResults.filter( hotel__city__icontains = parse_comma_trim[0] )
            city = parse_comma_trim[0]            
             
        else:
            
            #
            # hoping the length is 2 [ city, country ]
            #            
            first_term = parse_comma_trim[0]
            last_term = parse_comma_trim[-1]

            city = first_term

            #
            # check if second term is country
            #
            if last_term in name_to_cc:
                country_cc = name_to_cc[last_term]
                country_code = country_cc 
                
                if country_cc == 'us' and first_term in us_states_set and par_min == None:
                    #
                    # check State, US case.
                    # parentheses are important due to way data is presented
                    #
                    scoreResults = scoreResults.filter( hotel__country_cc1='us',
                                                         hotel__city__contains = '(' + first_term + ')' )
                elif par_min == None:
                    #
                    # Handles City,Country case
                    #
                    scoreResults = scoreResults.filter( hotel__country_cc1=country_cc,
                                                         hotel__city__contains = first_term )
                else:
                    print "Getting results from last case"
                    #
                    # handles all other cases
                    #                    
                    # City (State), US case
                    # City (Non-State) case (e.g Washington (D.C), US)
                    # City ( Some Province ), Country (e.g Paris (Ontario), Canada
                    #
                    scoreResults = scoreResults.filter( hotel__country_cc1=country_cc,
                                                         hotel__city__contains = city + " " + par_min )
                
            else:

                print "Could not find", last_term, "in countries"

                if par_min == None:                    

                    #
                    # For this case: just search for city only
                    #
                    scoreResults = scoreResults.filter( hotel__city__contains = first_term )
                else:

                    #
                    # Search with paranthesis inclusion and city term
                    #
                    scoreResults = scoreResults.filter( hotel__city__contains = first_term,
                                                          hotel__city_preferred__contains = par_min )

    #
    # extra total column for score ordering ( order by DESC )
    #
    total_str = construct_totalscore_columns( interests_bitmap )[0]
    finalRes = scoreResults.extra( select = { 'total': total_str }, order_by=('-total',))
    

    # filter stars if not None
    if stars != None:
        finalRes = finalRes.filter( hotel__hotel_class__gte = stars )

    #
    # Enqueue search requests
    #
    QueueRequestsManager.EnqueueSearchRequest( session_guid, cont_id, country_code, city, interest_map, surprise_me )

    return (finalRes, trimmed_query)

#
# Helper functions
#
def filter_scoreresults_no_min( interests_map ):
    """
        returns scoreResults filtered such that the interests chosen do not have the absolute MIN_SCORE
    """
    scoreResults = None
    for elt in score_column_names.keys():

        scoreInterestColumn = score_column_names[elt]
        
        if interests_map[elt] == True:
            if scoreResults == None:
                scoreResults  = Score.objects.extra( where = [scoreInterestColumn  + ' >  %s'], params = [MIN_SCORE])
            else:
                scoreResults = scoreResults.extra( where = [scoreInterestColumn  + ' >  %s'], params = [MIN_SCORE])
    return scoreResults

def construct_totalscore_columns( interests_map ):
    """
        Given interest_map ( interest:True ), return string for total score based on database columns for SQL query and count
        of how many interests chosen, and where clause for filter
        e.g for interests picked (shopping, family), return "shoppingScore + familyScore"  as first value of tuple and 2 as second value
        and third value will be shoppingScore > %s or familyScore > %s
    """
    s_total = ""
    count = 0
    s_where_clause = ""
    for elt in interests_map.keys():

        if interests_map[elt] == True:
            count += 1
            #
            # first column set
            #
            if s_total == "":
                s_total = score_column_names[elt]
                s_where_clause = score_column_names[elt] + ' > %s'
            else:
                s_total = s_total + " + " +  score_column_names[elt]
                s_where_clause = s_where_clause + " or " + score_column_names[elt] + ' > %s'
    
    return (s_total, count, s_where_clause)

def surpriseme_query( interests_map, scoreResults ):
    """
        Return query for surprise me feature given interests_map,
        and the filterd scoreRestuts for chosen interest where absolute values
        are not minimum

        This method assumes interest_map has at least one true input and that one
        True input should definitely have a result set of more than one element.

        Input:
            ScoreRestults: if not None, already filtered result
    """

    if (scoreResults == None):
        #
        # scores filtering
        #
        scoreResults = filter_scoreresults_no_min( interests_map )

    #
    # For no result case, overwrite an interest (ignore) and try again
    #
    if (len(scoreResults) == 0):
        for elt in interests_map.keys():
            if interests_map[elt] == True:
                interests_map[elt] = False
                print "elt punched out:", elt
                
                #
                # evalutate again by relaxing the restriction
                #
                scoreResults = filter_scoreresults_no_min( interests_map )
                
                #
                # check that the length is not zero
                #
                if len(scoreResults) != 0:
                    break
    #
    # extra total column for score ordering ( order by DESC )
    #
    total_str = construct_totalscore_columns( interests_map )
    result = scoreResults.extra( select = { 'total': total_str }, order_by=('-total',))[:MAX_SURPRISE_RES]

    random_res_picked = random.choice( result )

    cc = random_res_picked.hotel.country_cc1

    return (cc_to_name[cc], scoreResults)
