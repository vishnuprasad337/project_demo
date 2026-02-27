from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User,Hotel,Hotelbooking,Room
from django.db.models import Sum
from .serializers import UserSerializers,HotelSerializers,BookingSerializers,RoomSerializers
from django.shortcuts import render,get_object_or_404,redirect

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
class RoomsAddAPIView(APIView):
   

    def get(self, request, pk):
        
        try:
            hotel = Hotel.objects.get(id=pk)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
        
       
        rooms = hotel.rooms.all()
        serializer = RoomSerializers(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        try:
            hotel = Hotel.objects.get(id=pk)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found"}, status=404)

        if not isinstance(request.data, list):
            return Response({"error": "Send list of rooms"}, status=400)

        updated_rooms = []

        for room_data in request.data:
            room_type = room_data.get("room_type")
            price = room_data.get("price")
            available_rooms = room_data.get("available_rooms", 0)
            existing_room=Room.objects.filter(hotel=hotel,room_type=room_type).first()
            if existing_room:
                existing_room.available_rooms += int(available_rooms)
                if price:
                    existing_room.price = price

                existing_room.save()
            
            else:
            
                serializer = RoomSerializers(data=room_data)
                if serializer.is_valid():
                    serializer.save(hotel=hotel)
                    updated_rooms.append(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
          
        return Response(updated_rooms, status=201)
                
             


class BookingregisterAPIView(APIView):
    def post(self,request):
        serializers=BookingSerializers(data=request.data)
        if serializers.is_valid():
            room=serializers.validated_data['rooms']
            count=serializers.validated_data['count']
            starting_date=serializers.validated_data['check_in']
            ending_date=serializers.validated_data['check_out']
            duration = (ending_date - starting_date).days
            days = max(duration, 1)

           
            if duration<=0:
                return Response ( {"error: check_out must be after check_in" },status=400)

           
            if room.available_rooms < count:
                 return Response(
                {"error": f"Only {room.available_rooms} rooms available"},status=status.HTTP_400_BAD_REQUEST)
           
            total_amount= days*room.price*count
                
            room.available_rooms-=count
            room.save()
            
            

            balance_rooms = room.available_rooms
            booking = serializers.save(balance_rooms=balance_rooms,total_amount=total_amount)

            result=BookingSerializers(booking).data

            return Response(result, status=status.HTTP_201_CREATED)
        return Response (serializers.errors,status=404)
  
    def get(self,request):
        booking=Hotelbooking.objects.all()
        serializers=BookingSerializers(booking,many=True)
        return Response(serializers.data)
   
class BookingListAPIView(APIView):  
    def get_object(self, pk):
        try:
            return Hotelbooking.objects.get(pk=pk)
        except Hotelbooking.DoesNotExist:
            return None
    def get(self, request, pk):
        booking = self.get_object(pk)
        if not booking:
            return Response({"error": "booking not found"}, status=404)

        return Response(BookingSerializers(booking).data)

class BookingListhotelAPI(APIView):
    def get(self, request, hotel_id):
        bookings = Hotelbooking.objects.filter(hotel_id=hotel_id)
        serializer = BookingSerializers(bookings, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'bookingapp/index.html')
def user(request):    
    return render(request, 'bookingapp/user.html')
def hotel(request):    
    return render(request, 'bookingapp/hotel.html')
def hotel_login_view(request):
    return render(request, "bookingapp/hotel_login.html")

def hotel_list_view(request):
    hotels = Hotel.objects.all()
    return render(request, "bookingapp/hotel_list.html", {"hotels": hotels})
def hotel_rooms_view(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = hotel.rooms.all()

    return render(request, 'bookingapp/hotel_rooms.html', {
        'hotel': hotel,
        'rooms': rooms
    })
def hotel_login_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            hotel = Hotel.objects.get(name=name, password=password)

            request.session['hotel_id'] = hotel.id

            return redirect('hotel_dashboard')

        except Hotel.DoesNotExist:
            return render(request, 'bookingapp/hotel_login.html', {
                'error': 'Invalid Hotel Name or Password'
            })

    return render(request, 'bookingapp/hotel_login.html')
  
from django.shortcuts import get_object_or_404

def hotel_dashboard(request):
    hotel_id = request.session.get('hotel_id')

    if not hotel_id:
        return redirect('hotel_login')

    hotel = get_object_or_404(Hotel, id=hotel_id)

    return render(request, 'bookingapp/hotel_dashboard.html', {
        'hotel': hotel
    })
def hotel_rooms_dashboard(request):
    hotel_id = request.session.get('hotel_id')

    if not hotel_id:
        return redirect('hotel_login')

    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.all()

    return render(request, 'bookingapp/hotel_rooms_dashboard.html', {
        'hotel': hotel,
        'rooms': rooms
    })
def hotel_bookings_dashboard(request):
    hotel_id = request.session.get('hotel_id')

    if not hotel_id:
        return redirect('hotel_login')

    bookings = Hotelbooking.objects.filter(hotel_id=hotel_id)

    return render(request, 'bookingapp/hotel_bookings_dashboard.html', {
        'bookings': bookings
    })