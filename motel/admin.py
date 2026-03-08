from django.contrib import admin
from motel.models import Rooms
from motel.models import Room
from motel.models import UserAccount
from motel.models import ContactUs

class roomadmin(admin.ModelAdmin):
    list_display=( 'room_name','room_des','room_price','room_facilities','room_image')

admin.site.register(Rooms,roomadmin)
admin.site.register(Room)


admin.site.register(UserAccount)

admin.site.register(ContactUs)

