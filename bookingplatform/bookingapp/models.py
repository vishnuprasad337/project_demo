from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):

    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be 10 digits."
    )


    user_name=  models.CharField(max_length=100)
    Address= models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    phonenumber=models.IntegerField(max_length=10,validators=[phone_validator])
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}  {self.email}"
    
    


class Hotel(models.Model):

   
    name=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    hotel_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Room(models.Model):
     ROOM_CHOICES = (
        ('Normal', 'Normal'),
        ('2 star', '2 star'),
        ('5 star', '5 star'),
        ('delux', 'delux'),
    )
    
     hotel =models.ForeignKey(Hotel,on_delete=models.CASCADE)
     
     room_type = models.CharField(max_length=100, choices=ROOM_CHOICES , default='Normal')
     Price = models.DecimalField(max_digits=10,decimal_places=2)
     is_available = models.BooleanField(default=True)

     def __str__(self):
         return f"{self.hotel.name} - {self.room_type}"
    
    
 

class Hotelbooking(models.Model):

    
    room_type= models.ForeignKey(Room, on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    count = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    is_available =models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} {self.email}"
    
    