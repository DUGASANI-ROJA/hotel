
from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.log_in, name="login"),
    path('signup/', views.signup, name="signup"),
    path('add-details/', views.add_details, name="details"),
    path('bookroom/', views.book_room, name="bookroom"),
    path('reset/', views.reset_room, name="reset"),
    path('room changes/', views.room_changes, name="change"),
    path('room details/<int:room_id>/', views.room_details, name="room_details"),
]