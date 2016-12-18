from django import forms

MAX_DESTINATION_LENGTH = 500

class HotelSearchForm(forms.Form):
    """ This is the form for hotel search """

    # interests check boxes
    wellness = forms.BooleanField( required = False )
    romance = forms.BooleanField( required = False )
    casinos = forms.BooleanField( required = False )
    beachAndSun = forms.BooleanField( required = False )
    skiing = forms.BooleanField( required = False )
    shopping = forms.BooleanField( required = False )
    nightlife = forms.BooleanField( required = False )
    adventure = forms.BooleanField( required = False )
    family = forms.BooleanField( required = False )
    historyAndCulture = forms.BooleanField( required = False )

    # destination
    destination = forms.CharField(required = False,
                                  max_length=MAX_DESTINATION_LENGTH,
                                  widget=forms.TextInput(attrs={'placeholder': 'Continent, Country, or City'}))
    surpriseme = forms.BooleanField( required = False )

    # destination fields - names should match Google API attributes
    locality = forms.CharField( required = False, max_length=MAX_DESTINATION_LENGTH )  # locality is like a city ( Google API )
    country_short = forms.CharField( required = False, max_length = 2 ) # country_code
    administrative_area_level_1 = forms.CharField( required = False, max_length=MAX_DESTINATION_LENGTH ) # State / Province equivalence

    # check-in / check-out dates
    checkInDate = forms.DateField( required = True )
    checkOutDate = forms.DateField( required = True )

    # rooms / adults / children
    rooms = forms.IntegerField( min_value = 0, required = False )
    adults = forms.IntegerField( min_value = 0, required = False )
    children = forms.IntegerField( min_value = 0, required = False )
