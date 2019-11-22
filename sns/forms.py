from django import forms
from .models import Message, Group
from django.contrib.auth.models import User

class PostForm(forms.Form):
    content = forms.CharField(max_length=500, \
                              widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-', '-')] + [(item.title, item.title) \
            for item in Group.objects. \
            filter(owner__in=[user])],
        )


class GroupSelectForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-', '-')] + [(item.title, item.title) \
            for item in Group.objects.filter(owner=user)],
        )

class MembersForm(forms.Form):
    def __init__(self, user, members=[], vals=[], *args, **kwargs):
        super(MembersForm, self).__init__(*args, **kwargs)
        self.fields['members'] =  forms.MultipleChoiceField(
            choices = [(item.username, item.username) for item in members],
            widget = forms.CheckboxSelectMultiple(),
            initial=vals
        )

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=50)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['owner', 'title']


