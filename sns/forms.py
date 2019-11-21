from django import forms
from .models import Message, Group
from django.contrib.auth.models import User

#class MessageForm(forms.ModelForm):
#    class Meta:
#        model = Message
#        fields = ['owner', 'content']
#        #fields = ['owner', 'group', 'content']

class PostForm(forms.Form):
    content = forms.CharField(max_length=500, \
                              widget=forms.Textarea)
    #group = forms.CharField(max_length=500, \
    #                          widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        ### added
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-', '-')] + [(item.title, item.title) \
            for item in Group.objects. \
            #filter(owner__in=[user, public])],
            filter(owner__in=[user])],
        )
