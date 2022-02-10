from django.shortcuts import render
from . models import Message

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')
    messages = Message.objects.filter(room=room_name) #[10:] # just the last ten. Question how can we be sure they comme in inverse order?
    num_messages = len(messages)
    if len(messages)>10:
        messages = messages[num_messages-10:]

    return render(request, 'chat/room.html', {'room_name':room_name, 'username': username, 'messages': messages })