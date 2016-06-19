from django import forms

MAX_NAME_LEN = 100
MAX_LEN_MESSAGE = 500
MAX_USERNAME_LENGTH = 250
PASSWORD_MIN_LENGTH = 10

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

class LoginForm(forms.Form):
    username = forms.CharField( required = True,
                                max_length=MAX_USERNAME_LENGTH,                                
                                widget=forms.TextInput(attrs={'placeholder': 'myusername or myemail@mail.com'}))
    password = forms.CharField( required = True,
                                min_length = PASSWORD_MIN_LENGTH,
                                widget=forms.PasswordInput(attrs={'placeholder': 'X8df!90EO'}))
