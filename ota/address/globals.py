from sets import Set
import threading
#
# Globals address-related to be used by the service
#

#
# our Affiliate ID
#
BOOKING_AID = 912463

#
# states in US 
#
us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
	     'Kentuky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
	     'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
	     'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island','South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
	     'West Virginia', 'Wisconsin', 'Wyoming']

us_states_set = Set( us_states )

#
# continents -> id map
#
continents_to_id = { "Europe":6,
                     "Asia":8, 
                     "North America": 1,
                     "South America": 3,
                     "Australia": 9, 
                     "Africa": 5 };

#
# country_code to country_name cache
#
cc_to_name = {}

#
# name to country_code cache
#
name_to_cc = {}

#
# Global destination list - cache
#
global_destination_list = []

#
# Global lock for city / country enumerations
#
global_lock = threading.Lock()

#
# Global countries list
#
global_countries = []
