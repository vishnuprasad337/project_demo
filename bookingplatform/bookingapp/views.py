from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User,Hotel,Hotelbooking
from .serializers import UserSerializers,HotelSerializers

class UserListCreateAPIView(APIView):
    def get(self,request):
        user=User.objects.all()
        serializer=UserSerializers(user,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer= UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class UserDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "User not found"}, status=404)
        return Response(UserSerializers(user).data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "user not found"}, status=404)

        serializer = UserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not User:
            return Response({"error": "user not found"}, status=404)

        user.delete()
        return Response({"message": "Deleted"}, status=204)

class HotelRegisterAPIView(APIView):
    def get(self,request):
        hotel=Hotel.objects.all()
        serializers=HotelSerializers(hotel,many=True)
        return Response(serializers.data)
    def post(self,request):
        serializers=HotelSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response (serializers.data,status=201)
        return Response (serializers.errors,status=404)
class HotelListAPIView(APIView):
       def get_object(self,pk):
           try:
            return Hotel.objects.get(pk=pk)
           except Hotel.DoesNotExist:
            return None
           
       def get(self, request, pk):
        hotels = self.get_object(pk)
        if not hotels:
            return Response({"error": "hotel not found"}, status=404)
        return Response(HotelSerializers(hotels).data)

#class BookingAPIView(APIView):
    





