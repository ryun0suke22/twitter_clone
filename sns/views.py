from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message
from .forms import PostForm

def index(request):
    if(request.method == 'POST'):
        messages= get_your_message(request.user)
    else:
        messages= get_your_message(request.user)

    params = {
        'login_user': request.user,
        'contents': messages,
    }
    return render(request, 'sns/index.html', params)

def post(request):
    if(request.method == 'POST'):
        content = request.POST['content']
        msg = Message()
        msg.owner = request.user
        msg.content = content
        msg.save()
        messages.success(request, 'New message is posted!')
        return redirect(to='/sns')

    else:
        form = PostForm(request.user)

        params = {
            'login_user': request.user,
            'form': form,
        }
        return render(request, 'sns/post.html', params)

def get_your_message(owner):
    messages = Message.objects.filter(owner=owner)
    return messages
