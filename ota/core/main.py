from os import listdir
from os.path import isfile, join
from Tokenizers import *
from utils import *
from marker import *

TAB = "\t"
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

if __name__== "__main__":

    # init file paths / file lists

    hotels_path = FILES_ROOT + "/8ANdTVsOIl70v7JOZ3Acw"
    city_path = FILES_ROOT + "/cityData"
    airport_path=FILES_ROOT + "/airportsData"
    landmarks_path=FILES_ROOT + "/landmarksData"
    regions_path=FILES_ROOT + "/regionsData"
    
    hotel_files = [join(hotels_path,f) for f in listdir(hotels_path) if isfile(join(hotels_path, f))]
    
    airport_files = [join(airport_path,f) for f in listdir(airport_path) if isfile(join(airport_path, f))]
    
    city_files = [join(city_path,f) for f in listdir(city_path) if isfile(join(city_path, f))]
    
    landmark_files = [join(landmarks_path,f) for f in listdir(landmarks_path) if isfile(join(landmarks_path, f))]
    
    region_files = [join(regions_path,f) for f in listdir(regions_path) if isfile(join(regions_path, f))]

    # delimiter is tab
    delimiter = TAB
    skip_first_line = True

    # initialize all tokenizers
    landmarkTok = LandmarkTokenizer(delimiter, landmark_files, skip_first_line)
    cityTok = CityTokenizer(delimiter, city_files, skip_first_line)
    hotelTok = HotelTokenizer(delimiter, hotel_files, skip_first_line)
    regionTok = RegionTokenizer(delimiter, region_files, skip_first_line)
    airportTok = AirportTokenizer( delimiter, airport_files, skip_first_line)

    #initialize markers
    familyInterestsMrkr = FamilyInterestsMarker( None )

    # globals neede for end results    
    cc_to_country = {}    

    do_city_fill( cityTok, cc_to_country )
    do_landmark_fill( landmarkTok, cc_to_country )
    do_airport_fill( airportTok, cc_to_country ) 
    do_region_fill( regionTok, cc_to_country )    

    numHotels = 0    
    for hotel in hotelTok.gen_hotel_objs():
        familyScore = familyInterestsMrkr.score(hotel)        
        if familyScore >= 100:
            numHotels+=1
            print hotel.hotel_booking_id, hotel.hotel_url, familyScore
            #print hotel.hotel_booking_id, hotel.name, hotel.hotel_url, hotel.city, "familyScore=", familyScore
    print numHotels

        
    
##    print "starting Hotels data tokenization -----"
##    hotels_proc = 0
##    hotels_not_added = 0
##    for hotel in hotelTok.gen_hotel_objs():
##
##        # get country object from hash
##        cc = hotel.country_cc1
##        country = cc_to_country.get(cc)
##       
##        if country != None:
##            was_added = country.add_hotel( hotel.city, hotel )
##            hotels_proc+=1
##
##            if not was_added:
##                hotels_not_added+=1                
##        else:
##            print "country:", cc , "Not found"
##
##    print "hotels processed =", hotels_proc
##    print "hotels NOT added =", hotels_not_added
            
        
                
            

    

            
        
        
