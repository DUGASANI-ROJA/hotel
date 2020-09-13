from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    mobile_number = models.CharField(max_length=10)
    check_in = models.DateField()
    check_out = models.DateField()
    no_of_rooms = models.IntegerField(default=1)
    no_of_people = models.IntegerField()

    def __str__(self):
        return self.name


class Room(models.Model):
    occupancy_choices = (
        ('occupied', 'occupied'),
        ('not occupied', 'not occupied'),
    )
    types = (
        ("standard", "standard"),
        ("deluxe", "deluxe"),
        ("luxury", "luxury"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    occupancy = models.CharField(max_length=20, choices=occupancy_choices)
    room_number = models.CharField(max_length=3)
    room_type = models.CharField(max_length=10)
    room_size = models.IntegerField(default=2)

    def __str__(self):
        return self.room_number


# class CustomerRoomMapping(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
#     room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
#     feedback = models.CharField(max_length=200)
#
#     def __str__(self):
#         return str(self.customer.name)+str(self.room)