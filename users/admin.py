from django.contrib import admin

from users.models import (Client, OTP)
# Register your models here.

admin.site.register(OTP)
admin.site.register(Client)