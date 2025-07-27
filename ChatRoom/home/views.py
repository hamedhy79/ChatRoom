from django.shortcuts import render ,redirect # type: ignore
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from.models import Room, Topic, Message
from.forms import RoomForm, UserForm
from django.contrib import messages
# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Backend develpers'},
# ]

def LoginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist!", 'danger')
        
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
    context = {'page':page}    
    return render(request, 'home/login_register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def RegisterUser(request):
    # page = 'register'   
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # format for change somthing in fields not stright save in database
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        messages.add_message(request, messages.INFO, "You are registred!")
    else:
        messages.error(request, "somthing is wrong or An a error!", 'danger')
    return render(request, 'home/login_register.html',{'form':form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q)|
        Q(name__icontains = q)|
        Q(describtion__icontains = q)
        )
    topics = Topic.objects.all()[0:4]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:2]
    
    contex = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'home/home.html', contex)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        massage = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    
    context = {'room': room, 'room_message':room_message, 'participants':participants}          
    return render(request, 'home/room.html', context)


def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms
               , 'room_messages':room_messages, 'topics':topics}
    return render(request, 'home/profile.html', context)


@login_required(login_url = 'login')
def CreateRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create( # type: ignore
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            describtion = request.POST.get('describtion'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')       
    context = {'form': form, 'topics':topics}     
    return render(request, 'home/room_form.html', context)

@login_required(login_url = 'login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('you have not allowed it!')
    if request.method == 'POST':     
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name'),
        room.topic = topic,
        room.describtion = request.POST.get('describtion')
        
    # if request.method == 'POST':
    #     form = RoomForm(request.POST, instance=room)
    #     if form.is_valid():
        form.save()
        return redirect('home')
        
    return render(request, 'home/room_form.html', {'form':form}, {'topics':topics}, {'room':room})

@login_required(login_url = 'login')
def DeleteRoom(request, pk):
    room = Room.objects.get(id=pk)   
    
    if request.user != room.host:
        return HttpResponse('you have not allowed it!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'home/delete_room.html', {'obj':room})


@login_required(login_url = 'login')
def DdeleteMessage(request, pk):
    message = Message.objects.get(id=pk)   
    
    if request.user != message.user:
        return HttpResponse('you have not allowed it!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'home/delete_room.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    return render(request, 'home/update-user.html', {'form':form})

def topicspage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'home/topics.html', {'topics':topics})

def activities(request):
    room_message = Message.objects.all()
    return render(request, 'home/activity.html', {'room_message':room_message})