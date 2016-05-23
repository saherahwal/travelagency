from django.db import models
from os import listdir
from os.path import isfile, join
from Tokenizers import *
from utils import *
from marker import *
from threadpool import *


TAB = "\t"
COMMA =","
FILES_ROOT = "C:/Users/Saher/OneDrive/Documents/OnlineTravelAgent"

def do_city_fill(cityTok, cc_to_country):
    print "starting city data tokenization -----"
    for city in cityTok.gen_city_objs():
        cc = city.country_code
        if cc not in cc_to_country:
            country = CountryObj( cc )
            cc_to_country[cc] = country
            country.add_city(city)
        else:
            cc_to_country[cc].add_city(city)

def do_landmark_fill(landmarkTok, cc_to_country):
    print "starting landmark data tokenization -----"
    num_landmarks_added = 0
    num_landmarks_notadded = 0
    for landmark in landmarkTok.gen_landmark_objs():        
        
        # get country_code cc
        cc = landmark.country_code

        country = None
        if cc not in cc_to_country:            
            print "No country data available for:", cc
            num_landmarks_notadded+=1
        else:
            # add landmark to the city in country - if found
            country = cc_to_country[cc]
            added = country.add_landmark( landmark.city_name, landmark)

            # TODO: Fix non_added landmarks (change city_name matching)
            if not added:                
                num_landmarks_notadded+=1
            else:
                num_landmarks_added+=1

    print "landmarks NOT added=", num_landmarks_notadded
    print "landmarks added=", num_landmarks_added

def do_airport_fill( airportTok, cc_to_country ):
    print "starting Airport data tokenization -----"
    for airport in airportTok.gen_airport_objs():

        # get country object from hash
        cc = airport.country_code
        country = cc_to_country.get(cc)

        if country != None:
            country.add_airport(airport)
        else:
            print "Country not found:", cc

def do_region_fill( regionTok, cc_to_country ):
    print "starting Regions data tokenization -----"
    for region in regionTok.gen_region_objs():

        # get country object from hash
        cc = region.country_code
        country = cc_to_country.get(cc)

        if country != None:
            country.add_region(region)
        else:
            print "Country not found:", cc

def write_score_files( hotelTokenizer, genMarker, scoresFolder ):
    """
        Write scores in file batches s.t each file is acted upon by thread concurrently for DB insert
    """
    
    print "starting HotelScore data tokenuzation ----- "

    #
    # set max capacity per file and starting index
    #
    maxFileCapacity = 10000
    indexStart = 0
    
    scoresFile = scoresFolder + "/scoresfile_" + str(indexStart) + ".txt"
    f = open( scoresFile, 'w')
    f_noscores = open( scoresFolder + "/noscores.txt", 'w')
    
    numHotels = 0
    totalHotelsProcessed = 0
    hotelsWithNoScores = 0
    
    for hotel in hotelTokenizer.gen_hotel_objs():

        # scores
        scores = genMarker.score(hotel)

        # scores on the line
        csvScores = genMarker.__str__()
        lineOfText =  hotel.hotel_booking_id + "," + csvScores + '\n'
        
        f.write( lineOfText )
        numHotels += 1
        totalHotelsProcessed+=1

        if genMarker.isNoScoreAssigned():
            hotelsWithNoScores += 1
            f_noscores.write( lineOfText )

        if numHotels > maxFileCapacity:
            indexStart += 1
            scoresFile = scoresFolder + "/scoresfile_" + str(indexStart) + ".txt"
            f.close()
            numHotels = 0
            f = open( scoresFile, 'w')

    f_noscores.close()

    print "Total hotels processed", totalHotelsProcessed
    print "Hotels with no scores", hotelsWithNoScores        

if __name__== "__main__":

    # init file paths / file lists

    hotels_path = FILES_ROOT + "/8ANdTVsOIl70v7JOZ3Acw"
    city_path = FILES_ROOT + "/cityData"
    airport_path=FILES_ROOT + "/airportsData"
    landmarks_path=FILES_ROOT + "/landmarksData"
    regions_path=FILES_ROOT + "/regionsData"
    scores_write_path = FILES_ROOT + "/scores"

    # files paths init
    hotel_files = [join(hotels_path,f) for f in listdir(hotels_path) if isfile(join(hotels_path, f))]    
    airport_files = [join(airport_path,f) for f in listdir(airport_path) if isfile(join(airport_path, f))]    
    city_files = [join(city_path,f) for f in listdir(city_path) if isfile(join(city_path, f))]    
    landmark_files = [join(landmarks_path,f) for f in listdir(landmarks_path) if isfile(join(landmarks_path, f))]    
    region_files = [join(regions_path,f) for f in listdir(regions_path) if isfile(join(regions_path, f))]
    hotelscores_files = [join(scores_write_path,f) for f in listdir(scores_write_path) if isfile(join(scores_write_path, f))]

    print "hotelscore files = ", hotelscores_files

    # delimiter is tab
    delimiter = TAB
    skip_first_line = True

    # initialize all tokenizers
    landmarkTok = LandmarkTokenizer(delimiter, landmark_files, skip_first_line)
    cityTok = CityTokenizer(delimiter, city_files, skip_first_line)
    hotelTok = HotelTokenizer(delimiter, hotel_files, skip_first_line)
    regionTok = RegionTokenizer(delimiter, region_files, skip_first_line)
    airportTok = AirportTokenizer( delimiter, airport_files, skip_first_line)    

    # make list of hotel tokenizers for parallelism
    hotelTokList = [ HotelTokenizer(delimiter, [f], skip_first_line) for f in hotel_files ]
    hotelScoresTokList = [ HotelScoresTokenizer( COMMA, [f], False)  for f in hotelscores_files ]
    
    #initialize markers
    wellnessInterestsMarker = WellnessInterestsMarker( None )
    skiingInterestsMarker = SkiingInterestsMarker( None )
    shoppingInterestsMarker = ShoppingInterestsMarker( None )
    romanceInterestsMarker = RomanceInterestsMarker( None )
    clubbingInterestsMarker = ClubbingInterestsMarker( None )
    historyAndCultureInterestsMarker = HistoryAndCultureInterestsMarker( None )
    casinoInterestsMarker = CasinoInterestsMarker( None )
    beachAndSunInterestsMarker = BeachAndSunInterestsMarker( None )
    familyInterestsMrkr = FamilyInterestsMarker( None )
    adventureInterestMrkr = AdventureInterestsMarker( None )

    #marker list
    markerList = [wellnessInterestsMarker, skiingInterestsMarker, shoppingInterestsMarker,
                  romanceInterestsMarker, clubbingInterestsMarker, historyAndCultureInterestsMarker,
                  casinoInterestsMarker, beachAndSunInterestsMarker, familyInterestsMrkr, adventureInterestMrkr]

    genMarker = GeneralMarker( markerList )

    # globals needed for end results    
    cc_to_country = {}    

    # fill city / airport / landmark / region in-memory data.
    do_city_fill( cityTok, cc_to_country )
    do_landmark_fill( landmarkTok, cc_to_country )
    do_airport_fill( airportTok, cc_to_country ) 
    do_region_fill( regionTok, cc_to_country )    

    # write scores in file chunks
##    write_score_files( hotelTok, genMarker, scores_write_path )
    
    # make list of threads to run (1 per file)
##    threads = []
##    idx = 0
##    for hTok in hotelTokList:
##        threads.append( HotelModuleDBWriteNativeThread( idx, hTok, genMarker ) )
##        idx += 1
##
##    # start all the threads
##    for thread in threads:
##        thread.start()
##
##    # wait for all threads to complete
##    for thread in threads:
##        thread.join()

    scoreWriteThreads = []
    idx = 0
    for hScoreTok in hotelScoresTokList:
        scoreWriteThreads.append(  HotelScoresDBWriteThread(idx, hScoreTok ) )
        idx += 1

    #scoreWriteThreads[0].run()
    
    #start all threads in parallel
    for thread in scoreWriteThreads:
        thread.start()

    # wait for all to complete before return
    for thread in scoreWriteThreads:
        thread.join()

        
        
