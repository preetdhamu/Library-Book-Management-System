from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms import ModelForm
from accounts.models import Chat
class IssueBookForm(forms.Form):
     # it will make a direct drop down list fetch all books in a drop down menu
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name ", to_field_name="isbn", label="Book ( Name and ISBN )")
     # it will make a direct drop down list fetch all subscribers in a drop down menu
    name2 = forms.ModelChoiceField(queryset=models.Profile.objects.all(), empty_label="Name ", to_field_name="user", label="Subscribers Details( Name and Email )")

    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})

class ChatForm(forms.ModelForm):
    class Meta:
      # without this model=chat we does not able to see the chat page
      model=Chat
      # without this we does not able to see the dailogue box of chat 
      fields=('message',)
    #   fields.widget.attrs.update({'class':'form-control'})

class ReturnBookForm(forms.Form):
    
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name ", to_field_name="isbn", label="Book ( Name and ISBN )")
    isbn2.widget.attrs.update({'class': 'form-control'})
