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
        self.hotelTokenizerObj = hotelTokenizerObj        
        self.threadId = threadId

    def run( self ):
        print "STARTED thread", self.threadId

        # yield one score at a time
        for hotelScore in self.hotelScoresTok.gen_hotelscores_objs():

            hotel_booking_id = hotelScore.getHotelBookingId()

            # get hotel - in case already added
            hotelsRes = Hotel.objects.filter( hotel_booking_id = hotel_booking_id )

            if len(hotesRes) != 0:

                try:
                
                    scoresDbObj = Scores.objects.update_or_create( hotel = hotelsRes[0],
                                                                   familyScore = scores[ FAMILY ],
                                                                   adventureScore = scores[ ADVENTURE ],
                                                                   beachSunScore = scores[ BEACH_AND_SUN ],
                                                                   casinosScore = scores[ CASINOS ],
                                                                   historyCultureScore = scores[ HISTORY_CULTURE ],
                                                                   clubbingScore = scores[ CLUBBING ],
                                                                   romanceScore = scores[ ROMANCE ],
                                                                   shoppingScore = scores[ SHOPPING ],
                                                                   skiingScore = scores[ SKIING ],
                                                                   wellnessScore = scores[ WELLNESS ] )
                    
                except Exception as e:                    
                    print 'Exception error is : %s' % e  
            

class HotelModuleDBWriteNativeThread(Thread):
    
    def __init__( self, threadId, hotelTokenizerObj, generalMarkerObj ):
        Thread.__init__(self)
        self.hotelTokenizerObj = hotelTokenizerObj
        self.generalMarkerObj = generalMarkerObj
        self.threadId = threadId

    def run(self):

        print "STARTED thread", self.threadId

        con = mdb.connect(host=HOST, user=USER, passwd=PWD, db=DB)
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
            if hotel.maxrate == "":
                maxrate = SPECIAL_INVALID_RATE
            if hotel.minrate == "":
                minrate = SPECIAL_INVALID_RATE
            if hotel.preferred == "":
                preferred = SPECIAL_INVALID_RATE
            
            query = "INSERT INTO " + DB + "." + HOTELS_TABLE + "(created, modified, hotel_booking_id, name, address, state_zip, city, country_cc1, ufi, hotel_class, currency_code, minrate, maxrate, " \
                    "preferred, nr_rooms, longitude, latitude, public_ranking, hotel_url, photo_url, desc_en, desc_fr, desc_es, desc_de, desc_nl, desc_it, desc_pt, desc_ja," \
                    "desc_zh, desc_pl, desc_ru, desc_sv, desc_ar, desc_el, desc_no, city_unique, city_preferred, continent_id, review_score, review_nr) VALUES ( NOW(), NOW(), '%s','%s','%s',"\
                    " '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' ,'%s','%s','%s','%s','%s','%s','%s','%s', '%s', "\
                    " '%s','%s'); " % ( hotel.hotel_booking_id,
                                     hotel.name.replace("\'","*"),       
                                     hotel.address.replace("\'","*"),
                                     hotel.state_zip,
                                     hotel.city.replace("\'","*"),
                                     hotel.country_cc1,
                                     hotel.ufi,
                                     hotel.hotel_class,
                                     hotel.currency_code,
                                     minrate,
                                     maxrate,
                                     preferred,
                                     hotel.nr_rooms,
                                     hotel.longitude,
                                     hotel.latitude,
                                     hotel.public_ranking,
                                     hotel.hotel_url,
                                     hotel.photo_url,
                                     hotel.desc_en.replace("\'","*"),
                                     hotel.desc_fr.replace("\'","*"),
                                     hotel.desc_es.replace("\'","*"),
                                     hotel.desc_de.replace("\'","*"),
                                     hotel.desc_nl.replace("\'","*"),
                                     hotel.desc_it.replace("\'","*"),
                                     hotel.desc_pt.replace("\'","*"),
                                     hotel.desc_ja.replace("\'","*"),
                                     hotel.desc_zh.replace("\'","*"),
                                     hotel.desc_pl.replace("\'","*"),
                                     hotel.desc_ru.replace("\'","*"),
                                     hotel.desc_sv.replace("\'","*"),
                                     hotel.desc_ar.replace("\'","*"),
                                     hotel.desc_el.replace("\'","*"),
                                     hotel.desc_no.replace("\'","*"),
                                     hotel.city_unique.replace("\'","*"),
                                     hotel.city_preferred.replace("\'","*"),
                                     hotel.continent_id,
                                     hotel.review_score,
                                     hotel.review_nr )

            try:          
                cursor.execute(query)
                numHotels += 1                

                if numHotels > hotelCapacity:
                    cursor.execute("COMMIT;")
                    cursor.execute("START TRANSACTION;")
                    cursor.execute("BEGIN;")
                    numHotels = 0
                    
            except Exception as e:
                print query
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
        
