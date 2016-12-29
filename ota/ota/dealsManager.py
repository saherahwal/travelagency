#
# Manager class for deals
# NOTE: Deals Finder used from Booking.com Affiliate - 
# https://admin.booking.com/pc/product_dealfinder.html?ses=fc44c0a3345ad8b8fdca0af519b1fa58&partner_id=544106&product_type=dfl2 
#
import random

class SpecialDeal(object):

    def __init__(self, header, subheader, ins_script):
        self.header = header
        self.subheader = subheader
        self.ins_script = ins_script

    def getHeader( self ):
        return self.header
    
    def getSubheader( self ):
        return self.subheader;

    def getInsScript( self ):
        return self.ins_script


class SpecialDealsContainer( object ):

    specialDealsList = []

    def __init__(self, specialDealsList ):
        self.specialDealsList = specialDealsList

    def addDeal( self, specialDeal ):
        self.specialDealsList.append( specialDeal )

    def returnRandomDeals( self, n ):
        random.shuffle( self.specialDealsList )
        return self.specialDealsList[:n]

#
# Hardcode special Deals for v1
# Note: for all the ins_scripts to work, they need to be existent on booking.com partner
# center under Deals Finder header under Products
#

miami_florida_sd = SpecialDeal(  "Escape to Miami Beach", 
                                 "Take a break from work! Spend your weekend at the beach.",
                                 """<ins class="bookingaff" data-aid="1218635" data-target_aid="912463" data-prod="dfl2" data-width="300" data-height="400" data-dest_id="20023182" data-dest_type="city" data-df_checkin="5" data-df_duration="2">
                                    <!-- Anything inside will go away once widget is loaded. -->
                                    <a href="//www.booking.com?aid=912463">Booking.com</a>
                                </ins>
                                <script type="text/javascript">
                                    (function(d, sc, u) {
                                      var s = d.createElement(sc), p = d.getElementsByTagName(sc)[0];
                                      s.type = 'text/javascript';
                                      s.async = true;
                                      s.src = u + '?v=' + (+new Date());
                                      p.parentNode.insertBefore(s,p);
                                      })(document, 'script', '//aff.bstatic.com/static/affiliate_base/js/flexiproduct.js');
                                </script>""")

sanfransisco_cali_sd = SpecialDeal( "Weekend Getaway in California",
                                    "Experience the breathtaking beauty of the Bay Area.",
                                    """ <ins class="bookingaff" data-aid="1218636" data-target_aid="912463" data-prod="dfl2" data-width="300" data-height="400" data-dest_id="20015732" data-dest_type="city" data-df_checkin="5" data-df_duration="2">
                                        <!-- Anything inside will go away once widget is loaded. -->
                                        <a href="//www.booking.com?aid=912463">Booking.com</a>
                                    </ins>
                                    <script type="text/javascript">
                                        (function(d, sc, u) {
                                          var s = d.createElement(sc), p = d.getElementsByTagName(sc)[0];
                                          s.type = 'text/javascript';
                                          s.async = true;
                                          s.src = u + '?v=' + (+new Date());
                                          p.parentNode.insertBefore(s,p);
                                          })(document, 'script', '//aff.bstatic.com/static/affiliate_base/js/flexiproduct.js');
                                    </script>""" )

laketahoe_cali_sd = SpecialDeal( "Visit Lake Tahoe",
                                 "Start your adventure in Tahoe: Hike, bike, kayak, horseback and more.",
                                 """ <ins class="bookingaff" data-aid="1218638" data-target_aid="912463" data-prod="dfl2" data-width="300" data-height="400" data-dest_id="2465" data-dest_type="region" data-df_checkin="5" data-df_duration="2">
                                    <!-- Anything inside will go away once widget is loaded. -->
                                    <a href="//www.booking.com?aid=912463">Booking.com</a>
                                </ins>
                                <script type="text/javascript">
                                    (function(d, sc, u) {
                                      var s = d.createElement(sc), p = d.getElementsByTagName(sc)[0];
                                      s.type = 'text/javascript';
                                      s.async = true;
                                      s.src = u + '?v=' + (+new Date());
                                      p.parentNode.insertBefore(s,p);
                                      })(document, 'script', '//aff.bstatic.com/static/affiliate_base/js/flexiproduct.js');
                                </script>""")

vancouver_canada_sd = SpecialDeal( "Weekend Tour in Vancouver",
                                   "Enjoy the stunning views from the top of Grouse Mountain - the Peak of Vancouver ",
                                   """ <ins class="bookingaff" data-aid="1218639" data-target_aid="912463" data-prod="dfl2" data-width="300" data-height="400" data-dest_id="-575268" data-dest_type="city" data-df_checkin="5" data-df_duration="2">
                                        <!-- Anything inside will go away once widget is loaded. -->
                                        <a href="//www.booking.com?aid=912463">Booking.com</a>
                                    </ins>
                                    <script type="text/javascript">
                                        (function(d, sc, u) {
                                          var s = d.createElement(sc), p = d.getElementsByTagName(sc)[0];
                                          s.type = 'text/javascript';
                                          s.async = true;
                                          s.src = u + '?v=' + (+new Date());
                                          p.parentNode.insertBefore(s,p);
                                          })(document, 'script', '//aff.bstatic.com/static/affiliate_base/js/flexiproduct.js');
                                    </script>""")

banff_canada_sd = SpecialDeal( "Discover Banff, Alberta",
                               "Fill your weekend with hiking, skiing, and sightseeing. Visit Banff National Park.",
                               """ <ins class="bookingaff" data-aid="1218640" data-target_aid="912463" data-prod="dfl2" data-width="300" data-height="400" data-dest_id="-560592" data-dest_type="city" data-df_checkin="5" data-df_duration="2">
                                    <!-- Anything inside will go away once widget is loaded. -->
                                    <a href="//www.booking.com?aid=912463">Booking.com</a>
                                </ins>
                                <script type="text/javascript">
                                    (function(d, sc, u) {
                                      var s = d.createElement(sc), p = d.getElementsByTagName(sc)[0];
                                      s.type = 'text/javascript';
                                      s.async = true;
                                      s.src = u + '?v=' + (+new Date());
                                      p.parentNode.insertBefore(s,p);
                                      })(document, 'script', '//aff.bstatic.com/static/affiliate_base/js/flexiproduct.js');
                                </script>""")

montreal_canada_sd = SpecialDeal( "Explore Montreal, Quebec",
                                  "Discover the city's rich history in its aptly named Old Montreal neighborhood.",
                                  """ <ins class="bookingaff" data-aid="1218642" data-target_aid="912463" data-prod="dfl2" data-width="300" data-height="400" data-dest_id="-569541" data-dest_type="city" data-df_checkin="5" data-df_duration="2">
                                    <!-- Anything inside will go away once widget is loaded. -->
                                    <a href="//www.booking.com?aid=912463">Booking.com</a>
                                </ins>
                                <script type="text/javascript">
                                    (function(d, sc, u) {
                                      var s = d.createElement(sc), p = d.getElementsByTagName(sc)[0];
                                      s.type = 'text/javascript';
                                      s.async = true;
                                      s.src = u + '?v=' + (+new Date());
                                      p.parentNode.insertBefore(s,p);
                                      })(document, 'script', '//aff.bstatic.com/static/affiliate_base/js/flexiproduct.js');
                                </script>""")


g_specialDealsContainer = SpecialDealsContainer( [ miami_florida_sd, 
                                                  laketahoe_cali_sd, 
                                                  sanfransisco_cali_sd, 
                                                  vancouver_canada_sd, 
                                                  banff_canada_sd,
                                                  montreal_canada_sd ] )




