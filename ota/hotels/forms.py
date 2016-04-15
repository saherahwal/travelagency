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
    destination = forms.CharField(required = True,
                           max_length=MAX_DESTINATION_LENGTH,
                           widget=forms.TextInput(attrs={'placeholder': 'Continent, Country, or City'}))
    surpriseme = forms.BooleanField( required = False )

    # check-in / check-out dates
    checkInDate = forms.DateField( required = False )
    checkOutDate = forms.DateField( required = False )

    # rooms / adults / children
    rooms = forms.IntegerField( min_value = 0 )
    adults = forms.IntegerField( min_value = 0 )
    children = forms.IntegerField( min_value = 0 )
