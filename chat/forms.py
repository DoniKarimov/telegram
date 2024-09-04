from django import forms
from django.contrib.auth.models import User
        
from .models import *
              
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email' ] # '__all__'
        
        
         
class TasdiqlashForm(forms.ModelForm):
    class Meta:
        model = Tasdiqlash
        fields = ['code', 'user', 'expired_time']
        
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'birthday', 'tel']
        
        
        
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['rasm', 'profile']
        
        
class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name']        
        
class ChatMembersForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget = forms.CheckboxSelectMultiple)
    class Meta:
        model = Chat
        fields = ['members']

class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['sms', 'user','chat','rasm']        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=30)
                    
