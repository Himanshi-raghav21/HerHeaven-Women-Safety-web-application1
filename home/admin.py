from django.contrib import admin
from home.models import Contact, EmergencyContact
# Register your models here.
admin.site.register(Contact)
#new
admin.site.register(EmergencyContact)

