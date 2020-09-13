from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Customer, Room, User
from .forms import RoomForm

# Create your views here.


def index(request):
    if request.user.is_superuser:
        user=request.user
        customer_list = Customer.objects.all()
        room_list = Room.objects.exclude(occupancy='occupied')
        # datas = Company.objects.values('designation').annotate(count=Count('id'))
        return render(request, "api/index.html", {'customer_list': customer_list, 'room_list': room_list, "user": user})
    return HttpResponse('you are not allowed')


def log_in(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('index'))
            return HttpResponseRedirect(reverse('details'))
        else:
            return HttpResponse("failed")
    return render(request, 'api/login.html')


def signup(request):
    if request.method == 'POST':

        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST['email'],
        )

        return HttpResponseRedirect(reverse('login'))

    return render(request, 'api/signup.html')


@login_required(login_url='login')
def add_details(request):
    user = request.user
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    try:
        Customer.objects.get(user=request.user)
        return HttpResponseRedirect(reverse('bookroom'))
    except:
        if request.method == "POST":
            customer = Customer.objects.create(
                user=user,
                name=request.user.username,
                mobile_number=request.POST['phone'],
                check_in=request.POST['check_in'],
                check_out=request.POST['check_out'],
                no_of_rooms=request.POST['no_of_rooms'],
            )
            return HttpResponseRedirect(reverse('bookroom'))
    return render(request, "api/add-details.html", {"user": user})


@login_required(login_url='login')
def book_room(request, **kwargs):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    user = request.user
    customer = Customer.objects.get(user=user)
    roomlist = Room.objects.exclude(occupancy='occupied')
    msg = kwargs

    if request.method == "POST":

        rooms_list = request.POST.getlist('rooms[]')
        # if len(rooms_list) < customer.no_of_people/2:
        #     return HttpResponseRedirect(reverse("bookroom", kwargs={"msg": "require more rooms",}))
        lst = []
        # room=Room.objects.get(room_number=rooms[0])
        for room in rooms_list:
            room = Room.objects.get(room_number=room)
            room.customer = customer
            lst.append(room)
            room.occupancy = "occupied"
            room.save()

        return HttpResponse(lst)

    return render(request, "api/bookroom.html", {"user": user, "roomlist": roomlist, 'msg': msg})


@login_required(login_url='login')
def reset_room(request):
    if request.user.is_superuser:
        room_list = Room.objects.filter(occupancy='occupied')
        for room in room_list:
            room.occupancy = "not occupied"
            room.save()
        return HttpResponse('reset done')
    return HttpResponse('you dont have the permission to do it')


@login_required(login_url='login')
def room_changes(request):
    if request.user.is_superuser:
        user=request.user
        room_list = Room.objects.all()
        return render(request, "api/room-changes.html", {"room_list": room_list, "user": user})
    return HttpResponse('you dont have the permission to do it')


@login_required(login_url='login')
def room_details(request, room_id):
    if request.user.is_superuser:
        user = request.user
        room = Room.objects.get(id=room_id)
        if request.method == "POST":

            occupancy = request.POST["occupancy"]
            room_number = request.POST["room_number"]
            room_type = request.POST["room_type"]
            room_size = request.POST["room_size"]

            room.occupancy = occupancy
            room.room_number = room_number
            room.room_type = room_type
            room.room_size = room_size
            room.save()

            return HttpResponseRedirect(reverse('change'))
        return render(request, "api/room-details.html", {"room": room, "user": user})
    return HttpResponse('you dont have the permission to do it')