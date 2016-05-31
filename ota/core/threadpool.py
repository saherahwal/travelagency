# nasty hack to get import to work
import sys, os
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ota.settings")

from threading import Thread
from hotels.models import *
from utils import *
import MySQLdb as mdb
import django
import datetime


HOST = 'localhost'
USER = 'root'
PWD = 'svn123123'
DB = 'mytravelsdb'
HOTELS_TABLE = "hotels_hotel"
HOTELS_SCORES_TABLE = "hotels_score"

SPECIAL_INVALID_RATE = -1

#
# call django.setup since it is standalone app not through the server
#
# Documented: https://docs.djangoproject.com/en/1.8/topics/settings/
# #calling-django-setup-is-required-for-standalone-django-usage
# 
django.setup()

class HotelScoresDBWriteThread(Thread):

    def __init__( self, threadId, hotelScoresTok ):
        Thread.__init__(self)
        self.hotelScoresTok = hotelScoresTok        
        self.threadId = threadId

    def run( self ):
        print "STARTED thread", self.threadId

        con = mdb.connect(host=HOST, user=USER, passwd=PWD, db=DB, charset='utf8')
        cursor = con.cursor()
        cursor.execute("START TRANSACTION;")
        cursor.execute("BEGIN;")

        # careful this number needs to be less than maximum number of hotels in score file!
        # otherwise we never commit
        hotelScoreCapacity = 1000
        numHotelsScores = 0  

        # yield one score at a time
        for hotelScore in self.hotelScoresTok.gen_hotelscores_objs():
           
            hotel_booking_id = hotelScore.getHotelBookingId()
            scores = hotelScore.getScoresDict()

            # get hotel - in case already added
            selectQuery = "SELECT name,id FROM " + HOTELS_TABLE + " WHERE hotel_booking_id=%s;" 

            cursor.execute( selectQuery, (hotel_booking_id,) )
            row = cursor.fetchone()            
                        
            if row != None:
                
                hotel_id = row[1]
                
                queryAdd = "INSERT INTO " + DB + "." + HOTELS_SCORES_TABLE + "(created, modified, hotel_id, familyScore, adventureScore, beachSunScore," \
                           " casinosScore, historyCultureScore, clubbingScore, romanceScore, shoppingScore, skiingScore, wellnessScore) VALUES ( NOW(), NOW(), %s, %s, %s,"\
                           " %s, %s, %s, %s, %s, %s, %s, %s);"             
                
                try:          
                    cursor.execute(queryAdd, ( hotel_id,
                                               (scores[ FAMILY ]),
                                               (scores[ ADVENTURE ]),
                                               (scores[ BEACH_AND_SUN ]),
                                               (scores[ CASINOS ]),
                                               (scores[ HISTORY_CULTURE ]),
                                               (scores[ CLUBBING ]),
                                               (scores[ ROMANCE ]),
                                               (scores[ SHOPPING ]),
                                               (scores[ SKIING ]),
                                               (scores[ WELLNESS ]) ) )
                    
                    numHotelsScores += 1                

                    if numHotelsScores > hotelScoreCapacity:
                        cursor.execute("COMMIT;")
                        cursor.execute("START TRANSACTION;")
                        cursor.execute("BEGIN;")
                        numHotelsScores = 0
                    
                except Exception as e:
                    print queryAdd
                    print 'Exception error is : %s' % e               
                
        cursor.execute("COMMIT;")
        print "ENDED thread", self.threadId                                                                                
                              

class HotelModuleDBWriteNativeThread(Thread):
    
    def __init__( self, threadId, hotelTokenizerObj, generalMarkerObj ):
        Thread.__init__(self)
        self.hotelTokenizerObj = hotelTokenizerObj
        self.generalMarkerObj = generalMarkerObj
        self.threadId = threadId

    def run(self):

        print "STARTED thread", self.threadId

        con = mdb.connect(host=HOST, user=USER, passwd=PWD, db=DB, charset='utf8')
        cursor = con.cursor()
        cursor.execute("START TRANSACTION;")
        cursor.execute("BEGIN;")
        
        hotelCapacity = 50000
        numHotels = 0        
        
        # yield one hotel at a time
        for hotel in self.hotelTokenizerObj.gen_hotel_objs():

            # invalid maxrate/minrate if not specified
            maxrate = hotel.maxrate
            minrate = hotel.minrate
            preferred = hotel.preferred
            nr_rooms =  hotel.nr_rooms
            if hotel.maxrate == "":
                maxrate = SPECIAL_INVALID_RATE
            if hotel.minrate == "":
                minrate = SPECIAL_INVALID_RATE
            if hotel.preferred == "":
                preferred = SPECIAL_INVALID_RATE
            if hotel.nr_rooms == "":
                nr_rooms = SPECIAL_INVALID_RATE
            
            
            query = "INSERT INTO " + DB + "." + HOTELS_TABLE + "(created, modified, hotel_booking_id, name, address, state_zip, city, country_cc1, ufi, hotel_class, currency_code, minrate, maxrate, " \
                    "preferred, nr_rooms, longitude, latitude, public_ranking, hotel_url, photo_url, desc_en, desc_fr, desc_es, desc_de, desc_nl, desc_it, desc_pt, desc_ja," \
                    "desc_zh, desc_pl, desc_ru, desc_sv, desc_ar, desc_el, desc_no, city_unique, city_preferred, continent_id, review_score, review_nr) VALUES ( NOW(), NOW(), %s, %s, %s,"\
                    " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "\
                    " %s, %s); " 

            try:          
                cursor.execute(query,(hotel.hotel_booking_id,
                                      hotel.name,       
                                      hotel.address,
                                      hotel.state_zip,
                                      hotel.city,
                                      hotel.country_cc1,
                                      hotel.ufi,
                                      hotel.hotel_class,
                                      hotel.currency_code,
                                      minrate,
                                      maxrate,
                                      preferred,
                                      nr_rooms,
                                      hotel.longitude,
                                      hotel.latitude,
                                      hotel.public_ranking,
                                      hotel.hotel_url,
                                      hotel.photo_url,
                                      hotel.desc_en,
                                      hotel.desc_fr,
                                      hotel.desc_es,
                                      hotel.desc_de,
                                      hotel.desc_nl,
                                      hotel.desc_it,
                                      hotel.desc_pt,
                                      hotel.desc_ja,
                                      hotel.desc_zh,
                                      hotel.desc_pl,
                                      hotel.desc_ru,
                                      hotel.desc_sv,
                                      hotel.desc_ar,
                                      hotel.desc_el,
                                      hotel.desc_no,
                                      hotel.city_unique,
                                      hotel.city_preferred,
                                      hotel.continent_id,
                                      hotel.review_score,
                                      hotel.review_nr ))
                
                numHotels += 1                

                if numHotels > hotelCapacity:
                    cursor.execute("COMMIT;")
                    cursor.execute("START TRANSACTION;")
                    cursor.execute("BEGIN;")
                    numHotels = 0
                    
            except Exception as e:
                print query
                print "hotel_bk_id", hotel.hotel_booking_id
                print "hotel.name", hotel.name
                print "city", hotel.city
                print 'Exception error is : %s' % e                
                
        cursor.execute("COMMIT;")
        print "ENDED thread", self.threadId
                

class HotelModuleDBWriteThread(Thread):

    def __init__( self, threadId, hotelTokenizerObj, generalMarkerObj ):
        Thread.__init__(self)
        self.hotelTokenizerObj = hotelTokenizerObj
        self.generalMarkerObj = generalMarkerObj
        self.threadId = threadId

    def run( self ):
        print "STARTED thread", self.threadId

        numHotels = 0
        
        # yield one hotel at a time
        for hotel in self.hotelTokenizerObj.gen_hotel_objs():           
            
            # invalid maxrate/minrate if not specified
            maxrate = hotel.maxrate
            minrate = hotel.minrate
            if hotel.maxrate == "":
                maxrate = SPECIAL_INVALID_RATE
            if hotel.minrate == "":
                minrate = SPECIAL_INVALID_RATE

            try:           
                # create hotel DB object - calls Save()
                hotelDbObj = Hotel.objects.update_or_create( hotel_booking_id = hotel.hotel_booking_id,
                                                           name=hotel.name,        
                                                           address = hotel.address,
                                                           state_zip = hotel.state_zip,
                                                           city = hotel.city,
                                                           country_cc1 = hotel.country_cc1,
                                                           ufi = hotel.ufi,
                                                           hotel_class=hotel.hotel_class,
                                                           currency_code=hotel.currency_code,
                                                           minrate=minrate,
                                                           maxrate=maxrate,
                                                           preferred = hotel.preferred,
                                                           nr_rooms=hotel.nr_rooms,
                                                           longitude=hotel.longitude,
                                                           latitude=hotel.latitude,
                                                           public_ranking=hotel.public_ranking,
                                                           hotel_url=hotel.hotel_url,
                                                           photo_url=hotel.photo_url,
                                                           desc_en=hotel.desc_en,
                                                           desc_fr=hotel.desc_fr,
                                                           desc_es=hotel.desc_es,
                                                           desc_de=hotel.desc_de,
                                                           desc_nl=hotel.desc_nl,
                                                           desc_it=hotel.desc_it,
                                                           desc_pt=hotel.desc_pt,
                                                           desc_ja=hotel.desc_ja,
                                                           desc_zh=hotel.desc_zh,
                                                           desc_pl=hotel.desc_pl,
                                                           desc_ru=hotel.desc_ru,
                                                           desc_sv=hotel.desc_sv,
                                                           desc_ar=hotel.desc_ar,
                                                           desc_el=hotel.desc_el,
                                                           desc_no=hotel.desc_no,
                                                           city_unique=hotel.city_unique,
                                                           city_preferred=hotel.city_preferred,
                                                           continent_id=hotel.continent_id,
                                                           review_score=hotel.review_score,
                                                           review_nr=hotel.review_nr )                          
                
              
            except Exception as e:
                print "hotel_bk_id", hotel.hotel_booking_id
                print "lat,lon,minrate,maxrate", hotel.latitude, hotel.longitude, minrate, maxrate
                print 'Exception error is : %s' % e  

            numHotels+=1
            
        print "ENDED thread", self.threadId, "processed", numHotels, "hotels"       
        
