# These are the forms used to render user data onto their profile pages and the OTP confirmation page

from django import forms
from users.models import OTP, Client

'''
We start by importing Django forms and user database tables we created. 
We create an OTPForm class that inherits from the “forms.ModelForm” class, 
this class transforms our class into a form that interacts with a specific model or database table, in this case the “OTPForm” class will work with the OTP model.
The form will have one field called otp_code, which accepts a string with a maximum length of 6 characters, 
it overrides the inner class “Meta” where you link it with the model to be associated with, OTP, and the fields to interact with “otp_code”

'''
class OTPForm(forms.ModelForm):
    otp_code = forms.CharField(max_length=6)

    class Meta:
        model = OTP
        fields = ['otp_code']


class ClientUpdateForm(forms.ModelForm):
    '''
    We will make the email and phone filed mandatory
     by instantiating them inside the class as variables.
    '''
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=17)
    
    class Meta:
        model = Client
        fields= ['first_name', 'last_name', 'username', 'email', 'phone_number']
