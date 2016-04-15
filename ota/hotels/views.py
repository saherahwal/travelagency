from django.shortcuts import render
from hotels import forms as hotelForms


def search(request):

    #
    # non-binding
    #
    hotelSearchForm = hotelForms.HotelSearchForm()

    if request.method == 'POST':

        #
        # check form validity
        #
        if hotelSearchForm.is_valid():
            wellness = hotelSearchForm.cleaned_data['wellness']
            romance = hotelSearchForm.cleaned_data['romance']
            casinos = hotelSearchForm.cleaned_data['casinos']
            beachAndSun = hotelSearchForm.cleaned_data['beachAndSun']
            skiing = hotelSearchForm.cleaned_data['skiing']
            shopping = hotelSearchForm.cleaned_data['shopping']
            nightlife = hotelSearchForm.cleaned_data['nightlife']
            adventure = hotelSearchForm.cleaned_data['adventure']
            family = hotelSearchForm.cleaned_data['family']
            historyAndCulture = hotelSearchForm.cleaned_data['historyAndCulture']

            destination = hotelSearchForm.cleaned_data['destination']
            surpriseme = hotelSearchForm.cleaned_data['surpriseme']
            
            checkInDate = hotelSearchForm.cleaned_data['checkInDate']
            checkOutDate = hotelSearchForm.cleaned_data['checkOutDate']

            rooms = hotelSearchForm.cleaned_data['rooms']
            adults = hotelSearchForm.cleaned_data['adults']
            children = hotelSearchForm.cleaned_data['children']

            # TODO: finish me please

    elif request.method == 'GET':

        return render(request,
                      "index.html",
                      {'hotelSearchForm': hotelSearchForm})

    else:
        
        #
        # return error on Non-GET/ Non-POST request
        #
        return None
        
    
