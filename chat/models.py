from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


import random

class User(AbstractUser):
    
    STATUS=(    ('admin','Admin'),
                ("user","User"),
                ("assist","Assist") 
            )
    
    GENDER=(    ('male','Male'),
                ("female","Female"),  
            )

    gender = models.CharField(max_length=10,choices=GENDER,default='male')
    status=models.CharField(max_length=10, choices=STATUS,default='user')
    active=models.BooleanField(default=False, verbose_name='user_holati')
  
    def __str__(self):
        return self.username


class Tasdiqlash(models.Model):
    code =models.IntegerField(null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_confirm_code')
    expired_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.code}-{self.user.username}"
    
    def is_expired(self):
        return self.expired_time<timezone.now()
    

@receiver(post_save, sender=User)
def create_code(sender, instance, created, **kwargs):
    if created:
        code = ''
        for i in range(5):
            code += str(random.randint(1,9))
        code = int(code)
        
        expired_time=timezone.now()+timedelta(minutes=5)
        Tasdiqlash.objects.create(
            code = code,
            user = instance,
            expired_time = expired_time
        )
    return True     


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=170, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    tel = models.CharField(max_length=13, null=True, blank=True)


class ProfileImage(models.Model):
    rasm = models.ImageField(upload_to='user/')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_images')

    class Meta:
        ordering = ('id',)


class Chat(models.Model): 
    STATUS = (
            ('group',"Group"),
            ('channels',"Channels"),
            ('friends', "Friends")
            )

    status = models.CharField(max_length=30, choices=STATUS,default='Friends')
    members = models.ManyToManyField(User, related_name='members') 
    name = models.CharField(max_length=30, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    Admin=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Admin',null=True,blank=True)
    Admins=models.ManyToManyField(User,related_name='Admins')

    def __str__(self):
        return self.status + ' - ' + self.name
 


class Messages(models.Model):

    TUR = (
           ('text', 'Text'),
           ('rasm', 'Rasm'),     
    )
    msg_type = models.CharField(max_length=30, choices=TUR, default='text')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(null=True, blank = True)
    rasm = models.ImageField(upload_to='rasm', null=True, blank=True)
    sms = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.chat.name + ' - ' +self.sms[:10]
    
    class Meta:
        verbose_name = 'Xabar'
        verbose_name_plural = 'Xabarlar'
