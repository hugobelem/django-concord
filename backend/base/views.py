from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db.models import Q

from . models import Room, Topic, Message
from . forms import RoomForm


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower().strip()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
        
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower().strip()
            user.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'An error occured, ok?')
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    search = request.GET.get('search') \
    if request.GET.get('search') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=search) |
        Q(name__icontains=search) |
        Q(description__icontains=search)
        )

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics':topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    msg = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        msg = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'msg': msg, 'participants': participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_forms.html', context)


@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Get OUT!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_forms.html', context)


@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Get OUT!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Get OUT!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})