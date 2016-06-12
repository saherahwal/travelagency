from django import forms

MAX_NAME_LEN = 100
MAX_LEN_MESSAGE = 500

class ContactUsForm( forms.Form ):
    """ This is the form for contact-us by email """

    # Name
    name = forms.CharField( required = True,
                            max_length=MAX_NAME_LEN,
                            widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    # email
    email = forms.EmailField( required = True )

    # message
    message = forms.CharField( required = True,
                              max_length = MAX_LEN_MESSAGE,
                              widget=forms.Textarea)
