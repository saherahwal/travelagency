#
# hard-coded interests 
#
TRAVEL_INTERESTS = [ 'family', 'adventure', 'beach & sun', 'casinos',
                     'history & culture', 'clubbing', 'romance',
                     'shopping', 'skiing', 'wellness', 'cruise' ]

WELLNESS = "wellness"
SHOPPING = "shopping"
ROMANCE = "romance"
CLUBBING = "clubbing"
CASINOS = "casinos"
ADVENTURE = "adventure"
BEACH_AND_SUN = "beach_and_sun"
FAMILY = "family"
SKIING = "skiing"
HISTORY_CULTURE = "history_and_culture"


class TimeRange:
    
    def __init__( self, start_month, end_month ):
        self.start_month = start_month
        self.end_month = end_month

class Season:

    def __init__(self, name, time_range, hemisphere):
        self.name = name
        self.time_range = time_range
        self.hemisphere = hemisphere
 
class Interest:

    def __init__(self, name, seasons):
        self.name = name
        self.seasons = seasons
   

class CountryObj:
    
    def __init__( self, country_code ):
        self.country_code = country_code

        # maintain cities and regions in country
        self.cities = {}
        self.regions = {}
        self.airports = {}

    def add_city(self, city):
        """
            add city to the country only if not already added.
            Returns True if add_city already added before, False otherwise
        """
        if (city.city_fullname not in self.cities):
            self.cities[city.city_fullname] = city            
            return False
        return True

    def add_landmark(self, city_name, landmark):
        if self.cities.get(city_name) != None:            
            self.cities[city_name].add_landmark(landmark)
            return True
        return False

    def add_hotel(self, city_name, hotel):
        if self.cities.get(city_name) != None:            
            self.cities[city_name].add_hotel(hotel)            
            return True        
        return False

    def add_airport(self, airport):
        if airport.airport_name not in self.airports:            
            self.airports[airport.airport_name] = airport

    def add_region(self, region):
        if region.region_name not in self.regions:            
            self.regions[region.region_name] = region
    
    def __eq__( self, other ):
        if not isinstance(other, CountryObj):
            return False
        else:
            if self == other:
                return True
            else:
                return other.country_code == self.country_code

    def __hash__( self ):
        return hash( self.country_code )

class LandmarkObj:

    def __init__( self, landmark_id, landmark_name, city_name, country_code, booking_deeplink ):

        self.landmark_id = landmark_id
        self.landmark_name = landmark_name
        self.city_name = city_name
        self.country_code = country_code
        self.booking_deeplink = booking_deeplink

    def __str__(self):
        return "Landmark:{" + self.landmark_id + "}:" + self.landmark_name + "," + \
                self.city_name + "," + self.country_code

class CityObj:

    def __init__( self, city_fullname, number_of_hotels, country_code, ufi, booking_deeplink ):

        self.city_fullname = city_fullname
        self.number_of_hotels = number_of_hotels        
        self.country_code = country_code
        self.ufi = ufi
        self.booking_deeplink = booking_deeplink

        # init landmarks / hotels / airports
        self.landmarks = []
        self.hotels = []
        self.airports = []

        self.landmark_ids = {}
        self.hotel_ids = {}

    def add_landmark( self, landmark ):
        if landmark.landmark_id not in self.landmark_ids:
            self.landmarks.append(landmark)
            self.landmark_ids[landmark.landmark_id] = landmark.landmark_name

    def add_hotel( self, hotel ):
        if hotel.hotel_booking_id not in self.hotel_ids:
            self.hotels.append(hotel)
            self.hotel_ids[hotel.hotel_booking_id] = hotel.name            

    def __str__(self):
        return "City:{" + self.city_fullname + "}: ufi=" + self.ufi + "," + self.country_code

class RegionObj:

    def __init__( self, region_id, region_name, region_type, number_of_hotels, country_code, booking_deeplink):

        self.region_id = region_id
        self.region_name = region_name
        self.region_type = region_type
        self.number_of_hotels = number_of_hotels
        self.country_code = country_code
        self.booking_deeplink = booking_deeplink

        # init cities
        self.cities = []

    def add_city( self, city_name ):
        self.cities.append(city_name)

    def __str__(self):
        return "Region:{" + self.region_id + "}: name=" + self.region_name + ", type=" +\
                self.region_type + "," + self.country_code

class AirportObj:

    def __init__( self, airport_name, iata, number_of_hotels, country_code, booking_deeplink):

        self.airport_name = airport_name
        self.iata = iata
        self.number_of_hotels = number_of_hotels
        self.country_code = country_code
        self.booking_deeplink = booking_deeplink

    def __str__(self):
        return "Region:{" + self.airport_name + "}: iata=" + self.iata + \
                "," + self.country_code

class HotelScoreObj:
    """ This class represents the scores of interests for a particular hotel """

    def __init__(self, hotel_booking_id, scores_dict):

        ## init fields
        self.hotel_booking_id = hotel_booking_id
        self.scores_dict = scores_dict

    def getHotelBookingId( self ):
        return self.hotel_booking_id

    def getScoresDict( self ):
        return self.scores_dict;

    def __str__(self):
        st = ""
        st += "hotel_booking_id=" + str(self.hotel_booking_id) + ","

        for k,v in self.scores_dict.iteritems():
            st += k + ":" + v + ","

        return st[:-1]

class HotelObj:

    def __init__(self, hotel_booking_id, name, address, state_zip, city, 
                 country_cc1, ufi, hotel_class, currency_code,
                 minrate, maxrate, preferred, nr_rooms, longitude, latitude,
                 public_ranking, hotel_url, photo_url,
                 desc_en, desc_fr, desc_es, desc_de, desc_nl,
                 desc_it, desc_pt, desc_ja, desc_zh, desc_pl,
                 desc_ru, desc_sv, desc_ar, desc_el, desc_no,
                 city_unique, city_preferred,
                 continent_id, review_score, review_nr):

        ## initialize hotel fields
        self.hotel_booking_id=hotel_booking_id        
        self.name=name
        
        self.address = address
        self.state_zip = state_zip
        self.city = city
        self.country_cc1 = country_cc1
        self.ufi=ufi
        
        self.hotel_class=hotel_class
        
        self.currency_code=currency_code
        self.minrate=minrate
        self.maxrate=maxrate
        self.preferred = preferred
        self.nr_rooms=nr_rooms
        
        self.longitude=longitude
        self.latitude=latitude
        
        self.public_ranking=public_ranking
        
        self.hotel_url=hotel_url
        self.photo_url=photo_url

        self.desc_en=desc_en
        self.desc_fr=desc_fr
        self.desc_es=desc_es
        self.desc_de=desc_de
        self.desc_nl=desc_nl
        self.desc_it=desc_it
        self.desc_pt=desc_pt
        self.desc_ja=desc_ja
        self.desc_zh=desc_zh
        self.desc_pl=desc_pl
        self.desc_ru=desc_ru
        self.desc_sv=desc_sv
        self.desc_ar=desc_ar
        self.desc_el=desc_el
        self.desc_no=desc_no
        
        self.city_unique=city_unique
        self.city_preferred=city_preferred
        
        self.continent_id=continent_id
        
        self.review_score=review_score
        self.review_nr=review_nr

    def __str__(self):
        return "Hotel:{" + self.name + "}, city=" + self.city + "," + self.country_cc1
    
