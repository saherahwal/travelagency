from Queue import Queue
from threading import Thread
from core.utils import *
from hotels.models import *
from django.core.exceptions import ObjectDoesNotExist

MAX_QUEUE_SIZE = 1000

# initialize the queues and the Queue Manager
searchRequestsQueue = Queue( MAX_QUEUE_SIZE )
print "Created Search Reqeust Queue"

bookNowRequestQueue = Queue( MAX_QUEUE_SIZE )
print "Created BookNow Reqeust Queue"

class SearchRequestWrapper:

    def __init__( self, coorelation_id, continent_id, country_code, city, interest_map, surpriseme ):
        self.coorelation_id = coorelation_id
        self.continent_id = continent_id
        self.country_code = country_code
        self.city = city
        self.interest_map = interest_map
        self.surpriseme = surpriseme

    def getContinentId(self):
        return self.continent_id

    def getCountryCode(self):
        return self.country_code

    def getCity(self):
        return self.city

    def getSurpriseMe(self):
        return self.surpriseme

    def getCoorelationId( self ):
        return self.coorelation_id

    def getInterest( self, interest ):
        value = self.interest_map.get(interest)
        if value != None:
            return value
        return False

class BookNowRequestWrapper:
    
    def __init__( self, searchRequest_id, hotel_id ):
        self.searchRequest_id = searchRequest_id
        self.hotel_id = hotel_id 

    def getSearchRequestId(self):
        return self.searchRequest_id

    def getHotelId(self):
        return self.hotel_id

class QueueRequestsManager(object):
    """
    The queue request manager provides static methods for enqueue requests
    and dequeue to process
    """

    def __init__(self):
        """
            initialize consumer threads and start them
        """
        #
        # init thread classes
        #
        self.searchReqConsumer = SearchRequestsConsumer( 1 )
        self.bookNowReqConsumer = BookNowRequestsConsumer( 1 )

        #
        # start the threads
        #
        self.searchReqConsumer.start()
        self.bookNowReqConsumer.start()
        
    #
    # Enqueue operations
    #

    @staticmethod
    def EnqueueSearchRequest( coorelation_id, continent_id, country_code, city, interest_map, surprise_me ):
        item = SearchRequestWrapper( coorelation_id, continent_id, country_code, city, interest_map, surprise_me )
        searchRequestsQueue.put( item )

    @staticmethod
    def EnqueueBookNowRequest( searchRequest_id, hotel_id ):
        item = BookNowRequestWrapper( searchRequest_id, hotel_id )
        bookNowRequestQueue.put( item )    
   
#
# Consumer Threads Classes
#

class SearchRequestsConsumer(Thread):

    def __init__( self, threadId ):
        Thread.__init__(self)
        self.threadId = threadId

    def run( self ):

        while True:

            #
            # get the item from the queue - block until item
            # is available
            #
            searchRequest_item = searchRequestsQueue.get()

            #
            # Fetch data
            #
            coorelation_id = searchRequest_item.getCoorelationId()
            continent_id = searchRequest_item.getContinentId()
            country_code = searchRequest_item.getCountryCode()
            city = searchRequest_item.getCity()

            #
            # replace None with empty string for DB entry
            #
            if country_code == None:
                country_code = ""
            if city == None:
                city = ""

            familyInterest = searchRequest_item.getInterest( FAMILY )
            adventureInterest = searchRequest_item.getInterest( ADVENTURE )
            beachSunInterest = searchRequest_item.getInterest( BEACH_AND_SUN )
            casinosInterest = searchRequest_item.getInterest( CASINOS )
            historyCultureInterest = searchRequest_item.getInterest( HISTORY_CULTURE )
            clubbingInterest = searchRequest_item.getInterest( CLUBBING )
            romanceInterest = searchRequest_item.getInterest( ROMANCE )
            shoppingInterest = searchRequest_item.getInterest( SHOPPING )
            skiingInterest = searchRequest_item.getInterest( SKIING )
            wellnessInterest = searchRequest_item.getInterest( WELLNESS )
            
            surpriseme = searchRequest_item.getSurpriseMe()

            #
            # Django create - Insert into DB
            #
            searchRequestObj = SearchRequest.objects.create( coorelation_id=coorelation_id,
                                                             continent_id=continent_id,
                                                             country_code=country_code,
                                                             city=city,
                                                             familyInterest=familyInterest,
                                                             adventureInterest=adventureInterest,
                                                             beachSunInterest=beachSunInterest,
                                                             casinosInterest=casinosInterest,
                                                             historyCultureInterest=historyCultureInterest,
                                                             clubbingInterest=clubbingInterest,
                                                             romanceInterest=romanceInterest,
                                                             shoppingInterest=shoppingInterest,
                                                             skiingInterest=skiingInterest,
                                                             wellnessInterest=wellnessInterest,
                                                             surpriseme=surpriseme )
            print "object added to db", searchRequestObj
            
            #
            # signal task done
            # 
            searchRequestsQueue.task_done()
            
        
class BookNowRequestsConsumer(Thread):

    def __init__( self, threadId ):
        Thread.__init__(self)
        self.threadId = threadId

    def run( self ):

        while True:

            #
            # get the item from the queue - block until item
            # is available
            #
            bookNowRequest_item = bookNowRequestQueue.get()

            #
            # Fetch data
            #
            searchRequest_id = bookNowRequest_item.getSearchRequestId()
            hotel_id = bookNowRequest_item.getHotelId()

            try:
                
                hotelObj = Hotel.objects.get(  id = hotel_id )
                searchReqObj = SearchRequest.objects.get( id = searchRequest_id )

                #
                # Django create - insert into DB
                #
                bookNowReqObj = BookNowRequest.objects.create( hotel=hotelObj, searchRequest=searchReqObj )

            except ObjectDoesNotExist:
                print "Either Hotel or Search Request doesn't exist"
                print "Hotel Id", hotel_id
                print "Search Request Id", searchRequest_id

            #
            # signal task done
            # 
            bookNowRequestQueue.task_done()
            
