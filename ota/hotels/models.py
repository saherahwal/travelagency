from django.db import models
from common.models import TimeStampedModel
from uuidfield import UUIDField

class Hotel(TimeStampedModel):
    
    # booking.com hotel ID
    hotel_booking_id = models.IntegerField()
    
    name = models.CharField(max_length = 250)

    #address
    address = models.CharField(max_length = 500)
    state_zip = models.CharField(max_length = 50)
    city = models.CharField(max_length=93)

    #country and ufi 
    country_cc1 =  models.CharField(max_length = 4)
    ufi = models.IntegerField()  
        
    # hotel stars
    hotel_class = models.FloatField()

    # currency code
    currency_code = models.CharField(max_length = 3)

    # avg rates
    minrate = models.DecimalField( null = True, blank=True, max_digits = 13, decimal_places=3)
    maxrate = models.DecimalField( null = True, blank=True, max_digits = 13, decimal_places=3)
    preferred = models.NullBooleanField()
    
    nr_rooms = models.SmallIntegerField()
    longitude = models.DecimalField(max_digits = 18, decimal_places=15)
    latitude = models.DecimalField(max_digits = 18, decimal_places=15)
    public_ranking =  models.SmallIntegerField()
    hotel_url = models.CharField(max_length = 250)
    photo_url = models.CharField(max_length = 250)    

    #descriptions
    desc_en = models.TextField(blank=True)
    desc_fr = models.TextField(blank=True)
    desc_es = models.TextField(blank=True)
    desc_de = models.TextField(blank=True)
    desc_nl = models.TextField(blank=True)
    desc_it = models.TextField(blank=True)
    desc_pt = models.TextField(blank=True)
    desc_ja = models.TextField(blank=True)
    desc_zh = models.TextField(blank=True)
    desc_pl = models.TextField(blank=True)
    desc_ru = models.TextField(blank=True)
    desc_sv = models.TextField(blank=True)
    desc_ar = models.TextField(blank=True)
    desc_el = models.TextField(blank=True)
    desc_no = models.TextField(blank=True)

    #preferred and unique in city
    city_unique = models.CharField(max_length = 100)
    city_preferred = models.CharField(max_length = 100)

    continent_id = models.SmallIntegerField()

    #reviews
    review_score = models.SmallIntegerField()
    review_nr = models.SmallIntegerField()

class Score(TimeStampedModel):

    # foreign keys
    hotel = models.ForeignKey(Hotel, related_name="hotel")

    # scores
    familyScore = models.IntegerField()
    adventureScore = models.IntegerField()
    beachSunScore = models.IntegerField()
    casinosScore = models.IntegerField()    
    historyCultureScore = models.IntegerField()
    clubbingScore = models.IntegerField()
    romanceScore = models.IntegerField()
    shoppingScore = models.IntegerField()
    skiingScore = models.IntegerField()
    wellnessScore = models.IntegerField()

class SearchRequest( TimeStampedModel ):
    """
        Records of searches done by the users for analysis and understanding
    """
    # coorelation ID ( to coorelate booking now requests with searches )
    coorelation_id = UUIDField()
    
    # query search request
    continent_id = models.SmallIntegerField( null = True )
    country_code =  models.CharField(max_length = 4)
    city = models.CharField(max_length=93)
    
    # interests chosen
    familyInterest = models.BooleanField()
    adventureInterest = models.BooleanField()
    beachSunInterest = models.BooleanField()
    casinosInterest = models.BooleanField()
    historyCultureInterest = models.BooleanField()
    clubbingInterest = models.BooleanField()
    romanceInterest = models.BooleanField()
    shoppingInterest = models.BooleanField()
    skiingInterest = models.BooleanField()
    wellnessInterest = models.BooleanField()

    # surprise_me
    surpriseme = models.BooleanField()

class BookNowRequest( TimeStampedModel ):
    """
        Records of user clicks on Book now leading to Booking.com
        NOTE: doesn't mean the user actually booked.
    """    
    hotel = models.ForeignKey(Hotel, related_name="book_hotel")

    # coorelation ID ( to coorelate booking now requests with searches )
    coorelation_id = UUIDField()

class TopInterestLocation( TimeStampedModel ):
    """
        This table keeps track of hotel top locations and interests
        to be shown on first page for quick search offers
    """

    # interests applicable
    familyInterest = models.BooleanField()
    adventureInterest = models.BooleanField()
    beachSunInterest = models.BooleanField()
    casinosInterest = models.BooleanField()
    historyCultureInterest = models.BooleanField()
    clubbingInterest = models.BooleanField()
    romanceInterest = models.BooleanField()
    shoppingInterest = models.BooleanField()
    skiingInterest = models.BooleanField()
    wellnessInterest = models.BooleanField()

    # query string
    querystring = models.CharField( max_length = 500 )

    # description
    description = models.CharField( max_length = 500 )
    
