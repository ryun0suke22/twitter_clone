from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message, Group
from .forms import PostForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login')
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

@login_required(login_url='/admin/login')
def post(request):
    if(request.method == 'POST'):
        gr_name = request.POST['groups'] #add
        content = request.POST['content']
        print("gr_name", gr_name)
        ### added
        group = Group.objects.filter(owner=request.user) \
            .filter(title=gr_name).first()
        ###
        #msg_group = Message.objects.filter(group=group)
        #print('msg_group#####', msg_group)
        ###
        msg = Message()
        msg.owner = request.user
        msg.group = group #add
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
    #messages = Message.objects.filter(owner=owner)
    #return messages
    group = Group.objects.filter(owner=owner).first() # get the first item in Group
    messages = Message.objects.filter(group=group)
    return messages
