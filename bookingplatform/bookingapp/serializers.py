from rest_framework import serializers
from .models import User,Hotel,Hotelbooking,Room
from django.db.models import Sum

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model =User
        fields='__all__'
class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model =Hotel
        fields = ['id', 'name', 'city', 'hotel_type', 'password']
        extra_kwargs = {
            'password': {'write_only': True} 
            
        }
class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields=  fields = ['id','room_type', 'price', 'available_rooms']
       ## read_only_fields=['hotel']


   
class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotelbooking
        fields = [
            'id', 'hotel', 'rooms', 'room_type', 'name', 'email',
            'count', 'check_in', 'check_out', 'is_available', 'balance_rooms','total_amount'
        ]


    
    
