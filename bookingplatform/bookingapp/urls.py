from django.urls import path
from .views import *
urlpatterns=[

    path('api/users/', UserListCreateAPIView.as_view()),
    path('api/users/<int:pk>/', UserDetailsAPIView.as_view()),
    path('api/hotels/', HotelRegisterAPIView.as_view()),
    path('api/hotels/<int:pk>/',  HotelListAPIView.as_view()),
]

