from django import forms
from .models import Message
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['owner', 'content']

class PostForm(forms.Form):
    content = forms.CharField(max_length=500, \
                              widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        #public = User.objects.filter(username='public').first()
