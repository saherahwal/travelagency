from django.contrib import admin
from hotels.models import *

#
# model admin definitions
#
class TopInterestLocationAdmin(admin.ModelAdmin):
    list_display = ('description', 'querystring' )

class ScoreAdmin(admin.ModelAdmin):
    model = Score

    def hotel_booking_id(self, obj):
        return obj.hotel.hotel_booking_id

    def hotel_name(self, obj):
        return obj.hotel.name

    def hotel_url(self, obj):
        return obj.hotel.hotel_url
    
    list_display = ('hotel_booking_id', 'hotel_name', 'hotel_url',
                    'familyScore', 'adventureScore',
                    'beachSunScore', 'beachSunScore', 'casinosScore',
                    'historyCultureScore', 'clubbingScore', 'romanceScore',
                    'shoppingScore', 'skiingScore', 'wellnessScore' )

    list_filter = ( 'familyScore', 'adventureScore',
                    'beachSunScore', 'beachSunScore', 'casinosScore',
                    'historyCultureScore', 'clubbingScore', 'romanceScore',
                    'shoppingScore', 'skiingScore', 'wellnessScore' )

    hotel_name.admin_order_field = "hotel__name"


class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_booking_id', 'name', 'address', 'state_zip', 'city', 'country_cc1',
                    'desc_en', 'city_unique', 'city_preferred', 'continent_id', 'hotel_url', 'photo_url' )
    

# Register your models here.

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(TopInterestLocation, TopInterestLocationAdmin)
