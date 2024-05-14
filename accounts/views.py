from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout as lmn
from django.contrib.auth.decorators import login_required
from random import randrange
from .my_captcha import FormWithCaptcha
from .forms import IssueBookForm,ChatForm
from accounts.forms import IssueBookForm,ReturnBookForm
from datetime import date
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy
from .models import Chat
from django.utils import timezone

l=[]
# Create your views here.
# @login_required(login_url='')
@login_required
def home(request):
    return render(request,'home.html')
@login_required    
def home1(request):
    if request.method=='POST':
            searched=request.POST.get('searched')
            if len(searched)==0:
                messages.success(request, "Enter something")
            if searched.isnumeric():  
                books = Book.objects.filter(isbn__contains=int(searched))
            else:    
                books = Book.objects.filter(name__contains=searched)
                if not books:
                    messages.success(request, "Book Not Found") 
            return render(request,'hom1.html',{'searched':searched,'books':books})
    return render(request,'hom1.html')
def login_attempt(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        form=FormWithCaptcha(request.POST)
        user_object=User.objects.filter(username=username).first()
        if user_object is None:
            messages.success(request,'Username Not Found')
            return redirect('/')
        else:
            profile_obj=Profile.objects.filter(user=user_object).first()
            if not profile_obj.is_verified:
                messages.success(request,'Email is Not Verified Yet')
                return redirect('/')
            user=authenticate(username=username,password=password) 
            if user is None:
                messages.success(request,'Wrong Password')
                return redirect('/')
            if form.is_valid() :  
                if profile_obj.check_administrator: 
                    login(request,user)
                    return redirect('/home')
                else:
                    login(request,user)
                    return redirect('/home1')
            else:
                messages.success(request,'Pass the Recaptcha')
                return redirect('/')        
    return render(request,'login.html',{'a':FormWithCaptcha,})    

def register_attempt(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username is Already Taken')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                messages.success(request,'Email is Already Taken')
                return redirect('/register')
            user_obj=User.objects.create(username=username,email=email)  
            user_obj.set_password(password) 
            user_obj.save()
           
            auth_token=str(uuid.uuid4())
            # here we use uuid django web search it
            profile_obj=Profile.objects.create(user=user_obj,auth_token=auth_token) 
            profile_obj.save()
            send_mail_after_registraion(email,auth_token)
            return redirect('/token')
        except Exception as e:
            print(e)
    return render(request,'register.html')  
    
def success(request):
    return render(request,'success.html')      
def token_send(request):
    return render(request,'token_send.html')

def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your Account is Already Verified')
                return redirect('/')
            else:    
                profile_obj.is_verified=True
                profile_obj.save()
                messages.success(request,'Your Account Has Been Verified')
                return redirect('/')
        else:
            return redirect('/error') 
    except Exception as e:
        print(e)   
def send_mail_after_registraion(email,token):
    subject='Your Accounts Need To Be Verified'
    message=f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject, message,email_from, recipient_list)
def error_page(request):
    return render(request,'error.html')





def forget_pass(request):
    if request.method=='POST':
        email=request.POST.get('email')
        user_object=User.objects.filter(email=email).first()
        if user_object is None:
            messages.success(request,'Username Not Found')
            return redirect('/register')
        else:
            # profile_obj=Profile.objects.filter(user=user_object).first()
            otp=randrange(9999,999999)
            l.append(otp)
            l.append(email)
            send_otp_forget_password(email, otp)
            return redirect('/forget_auth_code')
    return render(request,'forget_pass1.html') 

def forget_auth_code(request):
    if request.method=='POST':
        otp1=request.POST.get('hcode')
        print(otp1,str(l[0]))
        if otp1==str(l[0]):
            messages.success(request,'Correct OTP')
            return redirect('/new_password') 
        else:
            messages.success(request,'Wrong OTP')
            return redirect('/forget')
    return render(request,'forget_pass2.html')

def new_password(request):
    try:
        if request.method=='POST':
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            user_object=User.objects.filter(email=str(l[1])).first()
            if user_object is None:
                messages.success(request,'Username Not Found')
                return redirect('/')
            if password1!=password2:
                messages.success(request,'Password not Match')
                return redirect('/')
            user_object=User.objects.get(email=str(l[1]))
            user_object.set_password(password1)
            user_object.save()
            messages.success(request,'UserName Found')
            return redirect('/')
    except Exception as e:
        print(e)
    return render(request,'new_password.html')


def send_otp_forget_password(email,otp):
    subject=f'OTP'
    message=f'Hello {email},Please OTP for reset your password request for E-library-{otp}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject, message,email_from, recipient_list)

@login_required
def add_book(request):
    if request.method=='POST':
        bookname=request.POST.get('bookname')
        authorname=request.POST.get('authorname')
        isbnnumber=request.POST.get('isbnnumber')
        category=request.POST.get('category')
        cover = request.FILES.get('cover')
        try:
            if Book.objects.filter(isbn=isbnnumber).first():
                messages.success(request,'Book is Already Taken')
                return redirect('/add_book')
            books=Book.objects.create(name=bookname,author=authorname,isbn=isbnnumber,category=category,cover=cover)   
            books.save()
            messages.success(request,'Book is Added')
            return redirect('/home')
        except Exception as e:
            print(e)
    return render(request,'add_book.html')
@login_required
def edit_book(request):
    if request.method=='POST':
            searched=request.POST.get('searched')
            
            if searched=='':
                messages.success(request, "Enter something")
            if searched.isnumeric():  
                books = Book.objects.filter(isbn__contains=int(searched))
            else:    
                books = Book.objects.filter(name__contains=searched)
                if not books:
                    messages.success(request, "Book Not Found")    
            return render(request,'edit_book.html',{'searched':searched,'books':books})   
    return render(request,'edit_book.html')

@login_required
def edit_book1(request,isbn):
    book=Book.objects.filter(isbn=isbn).first()

    if request.method=='POST':
        bookname=request.POST.get('bookname')
        authorname=request.POST.get('authorname')
        isbnnumber=request.POST.get('isbnnumber')
        category=request.POST.get('category')
        cover = request.FILES.get('cover')
        # update a book by making a null object 
        try:
            b=Book()
            b.id=book.id
            b.name=bookname
            b.author=authorname
            b.isbn=isbnnumber
            b.category=category
            b.cover=cover
            b.save()
            messages.success(request,"Book Updated Successfully")
            redirect('/home1')
        except Exception as e:
            print(e)
    return render(request,'edit_book1.html',{'books':book})    

@login_required
def view_books(request):
    books = Book.objects.all()
    messages.success(request,'All Books')
    return render(request,'view_books.html',{'book':books})    

@login_required
def view_subscribers(request):
    profiles = Profile.objects.all()

    return render(request, "view_subscribers.html", {'profiles':profiles})

@login_required
def issue_book(request):
    form=IssueBookForm()
    if request.method=='POST':
        form=IssueBookForm(request.POST)
        if form.is_valid():
            name2=request.POST['name2']
            isbn2=request.POST['isbn2']
            # to filter username of the given id 
            name2 = form.cleaned_data.get("name2")
            issued=IssuedBook.objects.filter(isbn=isbn2).first()
            if issued:
                messages.success(request,'Book Already Issued')    
            else: 
                book=Book.objects.filter(isbn=isbn2).first()   
                if name2.check_administrator==False :
                        obj=IssuedBook.objects.create(subscriber_username=str(name2.user),isbn=isbn2)
                        book.status='Y'
                        obj.save()
                        messages.success(request,'Book Issued To Subscribers Successfully')
                        redirect('/')
                else:
                    messages.success(request,"Book Can't be issued to a Administartion")
                    redirect('/view_issued_book')

    return render(request,'issuebook.html',{'form':form})

@login_required
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        messages.success(request,'All Issued Books')
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>30:  
            day=d-30
            fine=day*5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        user_object=User.objects.filter(username=i.subscriber_username).first()
        subscriber = list(models.Profile.objects.filter(user=user_object))
        print(subscriber)
        for y in books:
          t=(subscriber[0].user,books[0].name,books[0].isbn,i.issued_date,i.expiry_date,fine)
          details.append(t)
    return render(request,"view_issued_book.html",{'issuedBooks':issuedBooks, 'details':details})
@login_required
def delete_books(request, myid):
    # <built-in function id>
    try:
        books = Book.objects.filter(id=myid)
        if books.status=='N':
           books.delete()
           return redirect("/view_books")
    except Exception as e:
        print(e)    
    return render(request,"view_books.html")    

@login_required
def delete_subscribers(request, myid):
    subscriber = Profile.objects.filter(id=myid).first()
    issued_book = IssuedBook.objects.filter(subscriber_username=subscriber.user).first()
    if issued_book is None:
        subscriber.delete()
        redirect('view_subscribers')
    else:    
        print(issued_book.isbn)
        delete_issued_book(request,issued_book.isbn)
        subscriber.delete()
        redirect('view_subscribers')
    return redirect("/home")
@login_required
def delete_issued_book(request, isbn):
    try:
        issued_book = IssuedBook.objects.filter(isbn=isbn)
        issued_book.delete()
        return redirect("/view_issued_book")
    except Exception as e:
        print(e)    
    return render(request,"view_issued_book.html")


@login_required
def logout(request):
        lmn(request)
        messages.success(request, 'Log out Successfully')
        return redirect('/')        
@login_required
def subscriber_issued_books(request):
    print(request.user.username)
    issuedBooks = IssuedBook.objects.filter(subscriber_username=request.user.username)
    print(issuedBooks)

    details = []
    for i in issuedBooks:
        messages.success(request,'All Issued Books')
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>30:  
            day=d-30
            fine=day*5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        print(books)
        
        t=(books[0].name,books[0].isbn,i.issued_date,i.expiry_date,fine)
        details.append(t)
    return render(request,'subscriber_issued_books.html',{'details':details,})
@login_required 
def subscribe_view_book(request):
    books = Book.objects.all()
    messages.success(request,'All Books')
    return render(request,'subscribe_view_book.html',{'book':books})    






class UCreateChat(LoginRequiredMixin,CreateView):
    form_class=ChatForm
    model=Chat
    template_name='chat_form.html'
    success_url=reverse_lazy('UCreateChat')
    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return super().form_valid(form)

class UListChat(ListView):
	model = Chat
	template_name = 'chat_list.html'
   
	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')

class SCreateChat(LoginRequiredMixin,CreateView):
    form_class=ChatForm
    model=Chat
    template_name='chat_form_subscriber.html'
    success_url=reverse_lazy('SCreateChat')
    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return super().form_valid(form)

class SListChat(ListView):
	model = Chat
	template_name = 'chat_list_subscriber.html'
   
	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


def return_book(request):
    form=ReturnBookForm()
    t=[]
    if request.method=='POST':
        form=ReturnBookForm(request.POST)
        if form.is_valid():
            isbn2=request.POST['isbn2']
            t=list(ReturnChecker(request,isbn2))
    return render(request,'return_book.html',{'form':form,'list':t})

def confirm_return_book(request,isbn):
    try:
        issued_book = IssuedBook.objects.filter(isbn=isbn)
        book=Book.objects.filter(isbn=isbn).first()
        book.status='N'
        issued_book.delete()
        messages.success(request, 'Book returned Successfully')
    except Exception as e:
        print(e)    
    return render(request,'return.html')



def ReturnChecker(request,isbn):
    t=()
    issuedBooks = IssuedBook.objects.filter(subscriber_username=request.user.username,isbn=isbn)
    for i in issuedBooks:
        messages.success(request,'BOOK Found')
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>30:  
            day=d-30
            fine=day*5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        t=(books[0].name,books[0].isbn,i.issued_date,i.expiry_date,fine)
        break
    else:
        messages.success(request,f'Books Not issued by {request.user.username}')
    return t

    # return render(request,'subscriber_issued_books.html',{'details':details,})
    
#            

#             if IssuedBook.objects.filter(isbn=isbn2).first():
#                 messages.success(request,'Book Already Issued')    
#             else:    
#                 if name2.check_administrator==False:
#                     obj=IssuedBook.objects.create(subscriber_username=str(name2.user),isbn=isbn2)
#                     obj.save()
#                     messages.success(request,'Book Issued To Subscribers Successfully')
#                     redirect('/')
#                 else:
#                     messages.success(request,"Book Can't be issued to a Administartion")
#                     redirect('/view_issued_book')



def simple_checkout(request):
    return render(request, 'simple_checkout.html')


def book_view(request,isbn):
    return render(request,'book_view.html')    