from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User ,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100 )
    created_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)
    check_administrator=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username + " " + self.user.email
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='', null=True, blank=True) 
    status =models.CharField(max_length=10,default='N')
    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'


class IssuedBook(models.Model):
    subscriber_username = models.CharField(max_length=100) 
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=datetime.today() + timedelta(days=30))
    def __str__(self):
        return str(self.subscriber_username) + " ["+str(self.isbn)+']'


class Chat(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.TextField()
    posted_at=models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return str(self.message)