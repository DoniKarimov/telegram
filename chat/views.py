from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login,  authenticate
from django.utils import timezone
from django.contrib import messages
from chat.models import *                
from .forms import *
from django.views import View 

class Home(View):
    def get(self, request):
        chat_id = request.GET.get('chat_id')
        if chat_id:
            chat = Chat.objects.get(id=chat_id)
            for i in chat.messages.all():
                if not i.user == request.user:
                    i.is_read=True
                    i.save() 

        chats = Chat.objects.all()
        chat = None
        id = request.GET.get('chat_id')
        if id:
            chat = Chat.objects.get(id=id)
        azo = request.GET.get('azo')
        print(azo)

        if azo:
            chat = Chat.objects.get(id=azo)
            chat.members.add(request.user)
            chat.save()     
        return render(request, 'home.html', {'chats':chats, 'chat':chat})   
                 
        
    def post(self, request):
        form = MessagesForm()
        chat_id =request.POST.get('chat_id')
        sms = request.POST.get('sms')
        rasm = request.POST.get('rasm')   
        print('chat_id')
        print('sms')
        if chat_id:
            if request.POST:
                form = MessagesForm(request.POST, files=request.FILES)
                Messages.objects.create(
                       rasm = rasm,
                       user = request.user,  
                       chat = Chat.objects.get(id=chat_id)
                       
                    )
        sms = MessagesForm.objects.all()
             
        if sms:
            Messages.objects.create(
                sms = sms,      
                user = request.user,  
                chat = Chat.objects.get(id=chat_id)
            )
     
        chat_id = Chat.objects.get(id=chat_id)
        hammasi = Chat.objects.all()
        return render(request, 'home.html', {'chats':hammasi, 'chat':chat_id, 'form':form,})


# def messages_true(request, messages_id):
    
#     if request.POST:
#         message = Chat.objects.get(Messages, id=messages_id, user=request.user)
#         message.is_read = True
#         message.save()

#         return redirect('home')
#     return render(request, 'messages.html', {'message':message})
       

def create_channels(request):
    form = ChatForm()

    if request.POST:
        form = ChatForm(request.POST, files=request.FILES)
        if form.is_valid():
            Chat.objects.create(
             Admin=request.user,
             status = 'Channels',
             name = form.cleaned_data['name']
        )
        return redirect('home') 
    return render(request, 'create.html', {'form':form})   

def create_group(request):
    form = ChatForm()

    if request.POST:
        form = ChatForm(request.POST, files=request.FILES)
        if form.is_valid():
            Chat.objects.create(
                Admin = request.user,
                status = 'Group',
                name = form.cleaned_data['name']
            )
        return redirect('home')
    return render(request, 'create.html', {'form':form})


def register(request):
    form = UserForm()
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            w = form.save(commit=False)
            w.set_password(form.cleaned_data['password'])
            w.save()
            login(request, w)
            send_mail(
                      'doniyork513@gmail.com'
                       f'Salom, {w.username}!',
                       f'Sizning tasdiqlash kodingiz - {w.user_confirm_code.last().code}',
                       settings.EMAIL_HOST_USER,
                       [w.email],
                       fail_silently=False
                    )
            return redirect('home')
    return render(request, 'register.html', {'form': form})

def confirm(request):
    if request.POST:
        code = int(request.POST['code'])
        user = request.user
        if user.user_confirm_code.last().expired_time>timezone.now():
            if user.user_confirm_code.last().code == code:
                user.active=True
                messages.success(request, 'Siz tasdiqlandiz :) ')
                return redirect('home')
            else:
                messages.info(request, 'Sizning kiritgan kodingiz xato.')  
        else:
            messages.warning(request, 'Siz belgilangan vaqtdan otib ketdingiz..')  
    return render(request, 'confirm.html')


def profile(request):
    form = ProfileForm()
    
                 
    if request.POST:
        form = ProfileForm(request.POST, files=request.FILES, instance=request.user)
    if form.is_valid():
        Profile.objects.create(
                bio = form.cleaned_data['bio'],
                birthday = form.cleaned_data['birthday'],
                tel = form.cleaned_data['tel']
                )
                
        return redirect('home')
    return render(request, 'profile.html', {"form":form})


def created_name(request):
    form = ChatForm()
    if request.POST:
        form = ChatForm(request.POST)
        if form.is_valid():
            group = form.save()

            return redirect('add_members', group.id )
    return render(request, 'create.html', {'form':form})

def add_members(request,id):
    sms = MessagesForm()
    chat =Chat.objects.get(id=id)
    form = ChatMembersForm()

    if request.POST:
        form = ChatMembersForm(request.POST)
        userlar  = request.POST.getlist('members')
        for i in userlar:
           chat.members.add(i)
        chat.save()   
        return redirect('home')
    return render(request, 'create.html', {'form':form})


