from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message, Group
from .forms import PostForm, CreateGroupForm, GroupSelectForm, MembersForm
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
        gr_name = request.POST['groups']
        content = request.POST['content']
        group = Group.objects.filter(owner=request.user) \
            .filter(title=gr_name).first()
        msg = Message()
        msg.owner = request.user
        msg.group = group
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

def groups(request):
    members = User.objects.all()

    if request.method == 'POST':
        if request.POST['mode'] == '__groups_form__':
            sel_group = request.POST['groups']
            gp = Group.objects.filter(owner=request.user) \
                .filter(title=sel_group).first()
            mems = User.objects.get(username=request.user).group_owner.filter(title=gp)
            vlist = []
            for item in mems:
                vlist.append(item.owner)
            groupsform = GroupSelectForm(request.user, request.POST)
            membersform = MembersForm(request.user, members=members, vals=vlist)

        if request.POST['mode'] == '__members_form__':
            sel_group = request.POST['group']
            group_obj = Group.objects.filter(title=sel_group).first()
            vlist = request.POST.getlist('members')
            messages.success(request, ' チェックされたMemberを' + \
                             sel_group + 'に登録しました。')
            groupsform = GroupSelectForm(request.user, \
                                        {'groups': sel_group})
            membersform = MembersForm(request.user, \
                                      members=members, vals=vlist)

    else:
        groupsform = GroupSelectForm(request.user)
        membersform = MembersForm(request.user, members=members, \
                                  vals=[])
        sel_group = '-'

    createform = CreateGroupForm()

    params = {
        'login_user': request.user,
        'groups_form': groupsform,
        'members_form': membersform,
        'create_form': createform,
        'group': sel_group,
    }
    return render(request, 'sns/groups.html', params)

@login_required
def creategroup(request):
    gp = Group()
    gp.owner = request.user
    gp.title = request.POST['group_name']
    gp.save()
    messages.info(request, 'New group is created!')
    return redirect(to='/sns/groups')

def get_your_message(owner):
    gps = Group.objects.filter(owner=owner)
    glist = []
    for item in gps:
        glist.append(item)

    groups = Group.objects.filter(owner=owner).filter(title__in=glist)
    #restrict only 100 elements shown
    messages = Message.objects.filter(group__in=groups)[:100] 
    return messages
