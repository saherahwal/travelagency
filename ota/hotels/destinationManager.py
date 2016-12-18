#
# Manager class for destinations
#
from address.globals import cc_to_name 

class DestinationObj(object):
    """A class representing destination object"""
    
    def __init__( self, locality, country_short, administrative_area_level_1, continent = ""):
        self.city = locality
        self.country_code = country_short
        self.state = administrative_area_level_1
        self.continent = continent

    def getCity( self ):
        return self.city

    def getCountryCode( self ):
        return self.country_code

    def getState( self ):
        return self.state

    def isInUSA( self ):
        return self.country_code == 'us'

    def isInCanada( self ):
        return self.country_code == 'ca'

    def getContinent( self ):
        return self.continent

    def clearState( self ):
        self.state = ""
        return

    def clearCity( self ):
        self.city = ""
        return

    def getQueryDestTrimmed( self ):

        if self.continent != "":
            return self.continent.strip()
        else:
            city_state_country = ""
            if self.city != "" and self.city != None:
                city_state_country += (self.city + ", ") 
            if self.state != "" and self.state != None:
                city_state_country += (self.state + ", ")
            if self.country_code != "" and self.country_code != None:
                if self.country_code.lower() in cc_to_name:
                    city_state_country += (cc_to_name[self.country_code.lower()] + ", ")
                else:
                    city_state_country += (self.country_code + ", ")

            #
            # Remove extra trailing comma
            #
            city_state_country = city_state_country[:-2]
            return city_state_country


