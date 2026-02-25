from rest_framework import serializers
from .models import User,Hotel,Hotelbooking,Room

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model =User
        fields='__all__'
class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model =Hotel
        fields='__all__'
class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields='__all__'
class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotelbooking
        fields='__all__'