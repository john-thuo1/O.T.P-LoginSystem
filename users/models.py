from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tabnanny import verbose
# Create your models here.

class OTP(models.Model):
    otp_code = models.CharField(null=True, max_length=6)
    user = models.ForeignKey(User, related_name= 'OTPClient', on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.otp_code}'

    class Meta:
        verbose_name_plural = 'OTP'

#------------------------------------------------------------------------------------------------------------------------------  
'''
This table will hold the name of the registered users and their details, 
it will inherit from the User table its fields and also add a new field called phone to hold the users phone number
'''
class Client(User):
    phone_number = models.CharField(max_length=17)

    
    '''
    Apart from the Client table adding the phone field, 
    it overrides the method __str__ from its super class and returns 
    the user’s full name by calling the superclass’ get_full_name method.
    '''
    @property
    def full_name(self):
        return f'{super().get_full_name()}'
    
    
    def __str__(self):
        return f'{super().get_full_name()}'
    
    class Meta:
        verbose_name_plural = 'Client'
